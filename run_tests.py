"""
Modified test runner for state output injection. 
"""

import unittest
from importlib import import_module

# from state_injection import function_injection
import Levenshtein
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
        tests = unittest.defaultTestLoader.loadTestsFromModule(
            module
        )  # their function not mine

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
        """
        This takes in several test suites and runs all of the test cases inside the suite with recursion. 
        """
        # runner = unittest.TextTestRunner(stream = self.stdout_loc)
        result = unittest.TestResult()

        def run_test_case(test: unittest.TestCase):
            # if isinstance(test, unittest.TestCase): #this check is rendered unnecessary from below code
            test_id = test.id()  # Use the test's ID as a text value
            if os.path.isdir("state_output_logs"):
                to_delete = os.listdir("state_output_logs")
                for f in to_delete:
                    # should be jsonl if wanting to delete
                    if f.endswith(".json"):
                        os.remove(f)
            sys.stdout = open(f"state_output_logs/{test_id}.jsonl", "a")
            test(result)

        score = 0
        test_count = 0

        for test in self.test_suite:
            if isinstance(test, unittest.TestSuite):
                for sub_test in test:
                    # need this isinstance to not throw error in compare_to_gpt
                    if isinstance(
                        sub_test, unittest.TestCase
                    ):  # Iterate through sub-tests in the suite
                        run_test_case(sub_test)
                        score += self.compare_to_GPT(sub_test)
                        test_count += 1
            else:
                if isinstance(sub_test, unittest.TestCase):
                    run_test_case(test)
                    score += self.compare_to_GPT(test)
                    test_count += 1
        if test_count != 0:
            score /= test_count
        print("Score", score)

        # result = runner.run(self.test_suite)
        return result

    def compare_to_GPT(self, test: unittest.TestCase) -> float:

        """
        This function compares the test state extraction attained through the automatic generation and AST-based code with an LLM's generation of variable state extraction to determine how accurate the LLM's extraction is.  
        """
        
        test_id = test.id().split(".")
        #sys.stdout = self.stdout_loc
        score = 0
        gpt_output = []

        llm_test_root_path = f"{test_id[0]}/state_output_logs"

        for model_name in os.listdir(llm_test_root_path):
            llm_test_file_path = (
                llm_test_root_path
                + f"/{model_name}/"
                + f"{test_id[2]}.{test_id[3]}.json"
            )

            if os.path.isfile(llm_test_file_path):
                try:
                    with open(llm_test_file_path, "r") as f:
                        gpt_output = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from {llm_test_file_path}: {e}")
                    continue

                with open(f"state_output_logs/{'.'.join(test_id)}.jsonl", "r") as f:
                    correct_output = [json.loads(line) for line in f]
                    f.close()

                correct_index = -1
                total_lines = 0
                while correct_index < min(len(gpt_output), len(correct_output)) - 1:
                    correct_index += 1

                    gpt_out = gpt_output[correct_index]
                    total_lines += 1
                    correct_out = correct_output[correct_index]

                    # if gpt_out['file'].lower() != correct_out['file'].lower()
                    # or gpt_out['line_number'] != correct_out['line_number']: <- score will be even more like zero
                    if (
                        not isinstance(gpt_out, dict)
                        or "variables" not in gpt_out
                        or "code_line" not in gpt_out
                    ):
                        # correct_index += 1
                        # score is 0
                        continue

                    #Aligning lines as closesly as possible
                    if gpt_out["code_line"] not in correct_out["code_line"]:
                        for new_index in range(correct_index, len(correct_output)):
                            potential_match = correct_output[new_index]
                            if gpt_out["code_line"] in potential_match["code_line"]:
                                # Move correct_out to align with gpt_out
                                correct_index = new_index
                                correct_out = correct_output[new_index]
                                break
                        else:
                            # correct_index += 1
                            continue

                    #Determining score
                    var_titles = [field for field in correct_out if field in gpt_out and "variables" in str(field)]

                    for title in var_titles:

                        for var in correct_out[title]:
                            if var in gpt_out[title]:
                                ratio = Levenshtein.ratio(
                                    correct_out["variables"][var], gpt_out["variables"][var]
                                )
                            else:
                                ratio = 1
                            print(ratio)
                            score += ratio

                    score /= (
                        1
                        if len(correct_out["variables"]) == 0
                        else len(correct_out["variables"])
                    )

                    score /= (
                        1
                        if len(var_titles) == 0
                        else len(var_titles)
                    )

                    print("Comparison of outputs!")
                    print(gpt_out)
                    print(correct_out)

                score /= (
                        1
                        if total_lines == 0
                        else total_lines
                )

                #Saving score
                with open(f"{test_id[0]}/test_scores/{model_name}.txt", "a") as f:
                    f.write(f"{test_id[2]}.{test_id[3]}: {score}\n\n")

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
    if len(sys.argv) > 1:
        runner.load_tests_from_module(f"{sys.argv[1]}.tests")
        runner.run_tests()
    else:
        print("Specify which tests should be run!")
