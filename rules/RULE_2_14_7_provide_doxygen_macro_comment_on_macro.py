"""
Do not use macro for the constants.
if the constants is defined by macro. this rule reports a violation.
Instead, use enum or const variables.

However, it's ok to write a macro function.
And.. If the macro is start with underbar,
it regards this macro is defined for the special purpose
and it doesn't report a violation on it.

== Violation ==

    #define KK 1 <== Violation
    #define TT "sds" <== Violation

== Good ==

    #define KK(A) (A)*3 <== Don't care. It's macro function
    const int k = 3; <== OK
    const char *t = "EWEE"; <== OK
"""
from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_outputer import _consoleOutputer as console


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type == "PREPROCESSOR" and t.value.find("define") != -1:
        lexer.PushTokenIndex()
        t2 = lexer.GetPrevTokenInType("COMMENT")
        lexer.PopTokenIndex()
        if t2 is not None and t2.additional == 'DOXYGEN':
            return

        t2 = lexer.GetNextTokenSkipWhiteSpaceAndComment()

        if t2 is None or t2.type != "ID" or t2.lineno < 3:
            return

        while True:
            t3 = lexer.GetNextTokenInTypeList(['CPPCOMMENT', 'COMMENT'])

            if t3 is None or t2.lineno != t3.lineno:
                nsiqcppstyle_reporter.Error(t, __name__, "macro(%s) should comment" % t2.value)
                return

            if Search(r"/[/\*]{2}<", t3.value) or Search(r"/\**\*", t3.value) or Search(r"/\*!<", t3.value):
                return


ruleManager.AddPreprocessRule(RunRule)


##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddPreprocessRule(RunRule)

    def test1(self):
        self.Analyze("thisfile.c", """


#define k 1 ///< k
""")
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze("thisfile.c", """


#define tt(A) 3
///< tt(A)
""")
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze("thisfile.c", """


#  define t "ewew" /**< t */
""")
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze("thisfile.c", """


#define t 1 /*!< t */
""")
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze("thisfile.c", """

        

#define t 1 /* t taj*/
""")
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze("thisfile.c", """
/**
 * t
 */
#  define t "ewew" 
""")
        self.ExpectSuccess(__name__)

    def test7(self):
        self.Analyze("thisfile.c", """


/* t */
#  define t "ewew"
""")
        self.ExpectError(__name__)

    def test8(self):
        self.Analyze("thisfile.c", """

        
        
#define t 1
""")
        
        self.ExpectError(__name__)

    def test9(self):
        self.Analyze("thisfile.c", """

        

#define t 1 ///< t

#include <string.h>
                     """)
        self.ExpectSuccess(__name__)
