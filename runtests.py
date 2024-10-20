import unittest
from importlib import import_module
from state_injection import function_injection
import sys

class TestRunner:
    def __init__(self):
        self.test_suite = unittest.TestSuite()

    def add_test(self, test_case):
        self.test_suite.addTest(test_case)

    def load_tests_from_module(self, module_name):
        module = import_module(module_name)
        tests = unittest.defaultTestLoader.loadTestsFromModule(module)

        for test in tests:
            self.add_test(test)

    def run_tests(self):
        runner = unittest.TextTestRunner()
        result = runner.run(self.test_suite)
        return result

class ModifiedTestRunner(TestRunner):

    def recursively_add_tests(self, suite_to_add, modified_suite):
        for test in suite_to_add:
            if isinstance(test, unittest.TestSuite):
                modified_suite = self.recursively_add_tests(test, modified_suite)
            elif isinstance(test, unittest.TestCase):
                test_method = getattr(test, test._testMethodName)
                original_func = test_method.__func__

                modified_test_method = function_injection(original_func)
                print(modified_test_method)

                module_name = test.__class__.__module__
                module = sys.modules.get(module_name)
                if module is None:
                    print(f"Module {module_name} not found in sys.modules.")
                    exec_globals = {}
                else:
                    exec_globals = module.__dict__
                
                NewTestClass = type(f"Modified{test.__class__.__name__}", (test.__class__,), {})

                exec_namespace = exec_globals
                exec(modified_test_method, exec_namespace)

                #From chatgpt:

                new_test_method = exec_namespace[test._testMethodName]
                new_test_instance = NewTestClass(test._testMethodName)

                # Bind the new method to the instance
                bound_method = new_test_method.__get__(new_test_instance, NewTestClass)
                setattr(new_test_instance, test._testMethodName, bound_method)

                # Add the new test instance to the suite
                modified_suite.addTest(new_test_instance)


        return modified_suite

    def add_test(self, tests):
        modified_suite = unittest.TestSuite()
        modified_suite = self.recursively_add_tests(tests, modified_suite)
        self.test_suite.addTests(modified_suite)

if __name__ == '__main__':
    runner = ModifiedTestRunner()
    runner.load_tests_from_module('tests')
    runner.run_tests()
    