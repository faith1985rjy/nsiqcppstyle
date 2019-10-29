"""
switch should has default case.

== Violation ==

    void Function() {
        swtich(a) // <== Violation
        { 
        case 0:
        break;
        }
    }

== Good ==

    void Function()
    {
        switch(a)   //<== Good
        {
        case 0:
        break;
        default:
        break;
        }
    }

"""

from nsiqunittest.nsiqcppstyle_unittestbase import *
from nsiqcppstyle_reporter import *
from nsiqcppstyle_checker import *
from nsiqcppstyle_rulemanager import *
from nsiqcppstyle_outputer import _consoleOutputer as console


def RunRule(lexer, contextStack):
    t = lexer.GetCurToken()
    if t.type  == "SWITCH":
        lparen = lexer.GetNextTokenInType("LPAREN", False, True)
        if lparen is None:
            return
        lexer.GetNextMatchingToken()
        lbrace = lexer.GetNextTokenInType("LBRACE", False, True)
        lexer.PushTokenIndex()
        lexer.PushTokenIndex()
        t2 = lexer.GetNextMatchingToken()
        lexer.PopTokenIndex()
        count = 0
        while True:
            nextToken = lexer.GetNextTokenSkipWhiteSpaceAndCommentAndPreprocess()

            # console.Out.Ci(nextToken, nextToken.type)
            
            if nextToken is None or nextToken == t2:
                nsiqcppstyle_reporter.Error(t, __name__,
                        "switch should has default case.")
                break

            if nextToken.type == "DEFAULT" and count == 0:
                break

            if nextToken.type == "LBRACE":
                count = count + 1
            elif nextToken.type == 'RBRACE':
                count = count - 1
        lexer.PopTokenIndex()


ruleManager.AddFunctionScopeRule(RunRule)

##########################################################################
# Unit Test
##########################################################################


class testRule(nct):
    def setUpRule(self):
        ruleManager.AddFunctionScopeRule(RunRule)

    def test1(self):
        self.Analyze("thisfile.c", """
void function() {
    switch() {
    case 1:
    break;
    default:break;
    }
}
""")
        self.ExpectSuccess(__name__)

    def test2(self):
        self.Analyze("thisfile.c", """
void function() {
switch()
{
case 1:break;
}
}
""")
        self.ExpectError(__name__)


    def test3(self):
        self.Analyze("thisfile.c", """
void function() {
switch(true)
{
    case 1:
        switch(b)
        {
        case 2:
        break;
        default:
        break;
        }
        break;
}

}
""")
        self.ExpectError(__name__)

    def test4(self):
        self.Analyze("thisfile.c", """
void function() {
switch(true)
{
    case 1:
        switch(b)
        {
        case 2:
        break;
        }
        break;
    default:break;
}

}
""")
        self.ExpectError(__name__)

    def test5(self):
        self.Analyze("thisfile.c", """
void function() {
switch(true)
{
    case 1:
        switch(b)
        {
        case 2:
        break;
        default:break;
        }
        break;
    default:break;
}

}
""")
        self.ExpectSuccess(__name__)

    def test6(self):
        self.Analyze("thisfile.c", """
void functin(){
switch(a)
{
    case 1:
    {}
    case 2:
    {}
    default:
    {
    }
}
}                    
""")
        self.ExpectSuccess(__name__)
