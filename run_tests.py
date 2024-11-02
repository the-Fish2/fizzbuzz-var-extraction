"""
This is the file that runs the tests with a TestRunner, similar to what Django uses, and how to modify that to inject state output calls.
"""

import unittest
from importlib import import_module
from state_injection import function_injection
import sys


# This is how the tests are being run, which is pretty stock testrunner code with the python unittests library.
class TestRunner:
    def __init__(self):
        self.test_suite = unittest.TestSuite()

    def add_test(self, tests: unittest.TestSuite) -> None:
        for test in tests:
            self.test_suite.addTest(test)

    def load_tests_from_module(self, module_name: str) -> None:
        module = import_module(module_name)
        tests = unittest.defaultTestLoader.loadTestsFromModule(module)

        for test in tests:
            test_suite = unittest.TestSuite([test])
            self.add_test(test_suite)

    def run_tests(self) -> unittest.TestResult:
        runner = unittest.TextTestRunner()
        result = runner.run(self.test_suite)
        return result


# This is the modified version of the test runner, which includes the code for the function injection
class ModifiedTestRunner(TestRunner):

    # Adds suite tests one at a time after inserting state output function calls after every ast object
    def recursively_add_tests(
        self: "ModifiedTestRunner",
        suite_to_add: unittest.TestSuite,
        modified_suite: unittest.TestSuite,
    ) -> unittest.TestSuite:
        for test in suite_to_add:
            # Recursively iterating through the test suites and cases
            if isinstance(test, unittest.TestSuite):
                modified_suite = self.recursively_add_tests(test, modified_suite)
            else:
                test_method = getattr(test, test._testMethodName)
                original_func = test_method.__func__

                # State output, function injection comes from state_injection.py
                modified_test_method = function_injection(original_func)

                # Adding imports
                module_name = test.__class__.__module__
                module = sys.modules.get(module_name)
                if module is None:
                    print(f"Module {module_name} not found in sys.modules.")
                    exec_globals = {}
                else:
                    exec_globals = module.__dict__

                NewTestClass = type(
                    f"Modified{test.__class__.__name__}", (test.__class__,), {}
                )

                # Executing code so that when the method is next called, it gets the correct version
                exec_namespace = exec_globals
                exec(modified_test_method, exec_namespace)

                # From chatgpt: (Basically keeping the context of the initial method)
                new_test_method = exec_namespace[test._testMethodName]
                new_test_instance = NewTestClass(test._testMethodName)

                # Bind the new method to the instance
                bound_method = new_test_method.__get__(new_test_instance, NewTestClass)
                setattr(new_test_instance, test._testMethodName, bound_method)

                # Add the new test instance to the suite
                modified_suite.addTest(new_test_instance)

        return modified_suite

    # adding tests!
    def add_test(self, tests: unittest.TestSuite) -> None:
        modified_suite = unittest.TestSuite()
        modified_suite = self.recursively_add_tests(tests, modified_suite)
        self.test_suite.addTests(modified_suite)


if __name__ == "__main__":
    runner = ModifiedTestRunner()
    runner.load_tests_from_module("fizzbuzz_funcs.tests")
    runner.run_tests()

