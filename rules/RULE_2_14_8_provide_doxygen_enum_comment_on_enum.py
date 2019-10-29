"""
Indent the each enum item in the enum block.

== Violation ==

    enum A {
    A_A,  <== Violation
    A_B   <== Violation
    }


== Good ==

    enum A {
        A_A,///< A_A     <== Good
        A_B
    }
"""
from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_outputer import _consoleOutputer as console


def RunRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    if not decl and typeName == "ENUM" and typeContext is not None:
        lexer._MoveToToken(typeContext.startToken)
        while True:
            t = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            if t is None or t.type == 'RBRACE':
                break
            if t.type != 'ID':
                continue

            lexer.PushTokenIndex()
            t1 = lexer.GetNextTokenInTypeList(["CPPCOMMENT", "COMMENT"])
            if t1 is None or t1.lineno != t.lineno or (
                    t1.value.startswith("///<") == False 
                    and t1.value.startswith("/**<") == False
                    and t1.value.startswith("/*!<") == False):
                nsiqcppstyle_reporter.Error(t, __name__,
                        "enum(%s) item(%s) should comment." % (typeFullName, t.value))
            lexer.PopTokenIndex()


ruleManager.AddTypeNameRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddTypeNameRule(RunRule)

    def test1(self):
        self.Analyze("test/thisFile.c",
                     """
enum A {
A, ///< a
}
""")
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze("test/thisFile.c",
                     """
enum C {
    AA, ///< AA
    BB
}
""")
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze("test/thisFile.c",
                     """
enum C {
AA = 4,
    BB ///< BB
}
""")
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze("test/thisFile.c",
                     """
enum C {
    AA = 4 ///< AA
,BB,
}
""")
        self.ExpectError(__name__)

    def test5(self):
        self.Analyze("test/thisFile.c",
                     """
enum C {
    AA = 4 ///< AA
    ,BB,   ///< BB
}
""")
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze("thisfile.c", """
enum
{
    BMS_BHMRESOVERCNT_TIMERFLAG = 0,
    BMS_BRMRESOVERCNT_TIMERFLAG, ///< A
    BMS_BCPRESOVERCNT_TIMERFLAG, ///< B
    BMS_BRORESOVERCNT_TIMERFLAG, ///< C
};""")

        self.ExpectError(__name__)

    def test7(self):
        self.Analyze("test/thisFile.c",
                     """
typedef enum
{
  SERVICE, ///< SERVICE
  SERVER, /**< SERVER */
  BROKER, ///< BROKER
  MANAGER, ///< MANAGER
  REPL_SERVER, ///< REPL_SERVER
  REPL_AGENT, ///< REPL_AGENT
  UTIL_HELP, ///< UTIL_VERSION
  UTIL_VERSION, ///< UTIL_VERSION
  ADMIN,    ///< ADMIN
} UTIL_SERVICE_INDEX_E;
""")
        self.ExpectSuccess(__name__)


