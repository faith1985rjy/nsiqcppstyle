"""
Do not use more than 3 parameters in each function.
Use struct instead.
It checks function decl and impl together.
This rule is confused when the multiple template(KK<T, K>) is used in the parameter.
When you have to use such sentence, please // NS in the end of line to ignore this error.

== Violation ==

    void functionA(int a, int b, int c, int d); <== Violated, more than 3 parameters.

    void functionB(int a, int b, int c, int d, int e, int j)  <== Violated
    {
    }

== Good ==

    void functionA(int a, int b, int c); <== Good. 3 parameters.

    void functionB(int a, int b)  <== Good. 2 parameters
    {
    }

"""
from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_rulehelper import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_outputer import _consoleOutputer as console


def RunRule(lexer, fullName, decl, contextStack, context):
    lexer.GetNextTokenInType("LPAREN", False, True)
    lexer.PushTokenIndex()
    rparen = lexer.GetNextMatchingToken()
    lexer.PopTokenIndex()
    count = 0
    while(True):
        t = lexer.GetNextToken(True, True, True, True)
        if t.type == "COMMA":
            count += 1
        elif rparen == t:
            if count >= 3:
                nsiqcppstyle_reporter.Error(
                    t, __name__, "function (%s) has more than 3 parameters. please use struct instead." % fullName)
            break


ruleManager.AddFunctionNameRule(RunRule)


##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionNameRule(RunRule)

    def test1(self):
        self.Analyze("thisfile.c",
                     """
int functionA(int *a, int b, int d, Scope<T,J> a) {
}
""")
        self.ExpectError(__name__)

    def test2(self):
        self.Analyze("thisfile.c",
                     """
int functionA(int *a, int b,   Scope<T,J> a) {
}
""")
        self.ExpectError(__name__)

    def test3(self):
        self.Analyze("thisfile.c",
                     """
int functionA(int *a, tt&b, aa*s, k a) {
}
""")
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze("thisfile.c",
                     """
class T {
int functionA(int *a, int b, int c, tt&b) {
}
};
""")
        self.ExpectError(__name__)
