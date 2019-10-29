import unittest
import BSTestRunner

if __name__ == "__main__":
    discover = unittest.defaultTestLoader.discover('./rules', pattern='RULE_2_14_7*.py')
    with open('rules_unittest.html', 'w') as f:
        runner = BSTestRunner.BSTestRunner(stream=f, title="nsqicppstyle rules unit test", verbosity=2)
        runner.run(discover)
