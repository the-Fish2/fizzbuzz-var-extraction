"""
Modified test runner for state output injection. 
"""

import unittest
from importlib import import_module
# from state_injection import function_injection
import sys
import os
import json


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

    def __init__(self):
        super().__init__()
        self.stdout_loc = sys.stdout

    def run_tests(self) -> unittest.TestResult:
        # runner = unittest.TextTestRunner(stream = self.stdout_loc)
        result = unittest.TestResult()
        def run_test_case(test):
            if isinstance(test, unittest.TestCase):
                test_id = test.id()  # Use the test's ID as a text value
                if (os.path.isdir("state_output_logs")):
                    to_delete = os.listdir("state_output_logs")
                    for f in to_delete:
                        #should be jsonl if wanting to delete
                        if f.endswith('.json'): 
                            os.remove(f)
                sys.stdout = open(f"state_output_logs/{test_id}.jsonl", 'a')
                test(result)

        totalScore = 0;
        testCount = 0;

        for test in self.test_suite:
            if isinstance(test, unittest.TestSuite):
                for sub_test in test:  # Iterate through sub-tests in the suite
                    run_test_case(sub_test)
                    score += self.compare_to_GPT(sub_test)
                    testCount += 1
            else:
                run_test_case(test)
                score += self.compare_to_GPT(test)
                testCount += 1
            
        score /= testCount
        print(score)   

        #result = runner.run(self.test_suite)
        return result
    
    def compare_to_GPT(self, test: unittest.TestCase) -> float:
        testId = test.id().split(".")
        gptOutput = []

        if (os.path.isfile(f'{testId[0]}/state_output_logs/{testId[3]}.jsonl')):
            with open(f'{testId[0]}/state_output_logs/{testId[3]}.jsonl', 'r') as f:
                gptOutput = [json.loads(line) for line in f]

            with open(f"state_output_logs/{'.'.join(testId)}.jsonl", 'r') as f:
                correctOutput = [json.loads(line) for line in f]

            score = min(len(gptOutput), len(correctOutput))

            for gptO, correctO in gptOutput, correctOutput:
                if gptO['file'] != correctO['file'] or gptO['variables'] != correctO['variables'] or gptO['line_number'] != correctO['line_number']:
                    score -= 1
                
                #Very easy for misaligned output (ie, first line output in file 1 might be different from file 2)
                print(gptO)
                print(correctO)
            
            score /= max(len(gptOutput), len(correctOutput))

            print(score)
            return score
    
        return -1

    # Adds suite tests one at a time after inserting state output function calls after every ast object
    def recursively_add_tests(
        self: "ModifiedTestRunner",
        suite_to_add: unittest.TestSuite,
        modified_suite: unittest.TestSuite,
    ) -> unittest.TestSuite:

        for test in suite_to_add:
            # Recursively iterating through the test suites and cases
            modified_suite.addTest(test)

            # if isinstance(test, unittest.TestSuite):
            #     modified_suite = self.recursively_add_tests(test, modified_suite)
            # else:
            #     test_method = getattr(test, test._testMethodName)
            #     original_func = test_method.__func__

            #     # State output, function injection comes from state_injection.py
            #     modified_test_method = function_injection(original_func)

            #     # Adding imports
            #     module_name = test.__class__.__module__
            #     module = sys.modules.get(module_name)
            #     if module is None:
            #         print(f"Module {module_name} not found in sys.modules.")
            #         exec_globals = {}
            #     else:
            #         exec_globals = module.__dict__

            #     NewTestClass = type(
            #         f"Modified{test.__class__.__name__}", (test.__class__,), {}
            #     )

            #     # Executing code so that when the method is next called, it gets the correct version
            #     exec_namespace = exec_globals
            #     exec(modified_test_method, exec_namespace)

            #     # From chatgpt: (Basically keeping the context of the initial method)
            #     new_test_method = exec_namespace[test._testMethodName]
            #     new_test_instance = NewTestClass(test._testMethodName)

            #     # Bind the new method to the instance
            #     bound_method = new_test_method.__get__(new_test_instance, NewTestClass)
            #     setattr(new_test_instance, test._testMethodName, bound_method)

            #     # Add the new test instance to the suite
            #     modified_suite.addTest(new_test_instance)

        return modified_suite

    # adding tests!
    def add_test(self, tests: unittest.TestSuite) -> None:
        modified_suite = unittest.TestSuite()
        modified_suite = self.recursively_add_tests(tests, modified_suite)
        self.test_suite.addTests(modified_suite)


if __name__ == "__main__":
    runner = ModifiedTestRunner()
    if (len(sys.argv) > 1):
        runner.load_tests_from_module(f'{sys.argv[1]}.tests')
        runner.run_tests()
    else:
        print("Specify which tests should be run!")

