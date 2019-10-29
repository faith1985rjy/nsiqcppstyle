"""
Indent the each enum item in the enum block.

== Violation ==

    struct A {
    struct S a;  <== Violation
    int A_B;  <== Violation
    }


== Good ==

    struct A {
        int A_A; ///< A_A     <== Good
        int A_B; ///< A_B
    }
"""
from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_outputer import _consoleOutputer as console


def RunRule(lexer, typeName, typeFullName, decl, contextStack, typeContext):
    if not decl and typeName == "STRUCT" and typeContext is not None:
        lexer._MoveToToken(typeContext.startToken)
        t = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
        while True:
            t = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()
            if t is None:
                break

            if t.type != 'SEMI':
                continue
            t = lexer.GetNextTokenSkipWhiteSpace()
            if t is None or t.type not in {"CPPCOMMENT", "COMMENT"} or (t.value.startswith("///<") == False 
                                                       and t.value.startswith("/**<") == False):
                nsiqcppstyle_reporter.Error(t, __name__,
                        "struct(%s) item(%s) should comment." % (typeFullName, t.value))


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
struct A {
int A; ///< a
}
""")
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze("test/thisFile.c",
                     """
struct C {
   int AA; ///< AA
   int BB;
}
""")
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze("test/thisFile.c",
                     """
struct C {
struct S AA; ///< AA
 int BB; ///< BB
}
""")
        self.ExpectSuccess(__name__)

    def test4(self):
        self.Analyze("test/thisFile.c",
                     """
struct C {
    int AA; ///< AA
#define A
    int BB; ///< BB
}
""")
        self.ExpectSuccess(__name__)

    def test5(self):
        self.Analyze("test/thisFile.c",
                     """
struct C {
    int AA; ///< AA
    struct B {
        int a; ///< a
        int b; ///< b
    } BB; ///< BB
}
""")
        self.ExpectSuccess(__name__)



