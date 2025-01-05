from llm_interface.gpt_model import GPTModel, TogetherModel  # type:ignore
import subprocess
import os
import json
from llm_interface.state_extraction import StateExtractionFormat


def gen(model, prompt, sys_prompt=""):
    messages = model.create_message(prompt, sys_prompt)
    response = model.generate_text(messages)
    return response


def gpt_gen_code(model, alg):
    sys_prompt = "Write only a piece of code with no text that represents the skill of an intermediate coder."
    prompt = "Return only Python code that provides a working implementation of " + alg
    prompt += f" defined as \n def {alg.lower()}:"
    # assuming this is def alg (in all lowercase)
    return isolate_code(gen(model, prompt, sys_prompt), "python")


def gpt_gen_unit_test(model, code, alg):
    sys_prompt = "Write only a piece of code with no text."
    prompt = (
        "Please write several unit tests for this code in one testcase "
        + code
        + " in the following format: "
    )
    prompt += f""" 
        import unittest
        from code.{alg} import {alg.lower()}

        class Test{alg}(unittest.TestCase):
            def test_1:
                #test 1
            def test_2:
                #test_2

        This should be the only code returned. 
        """
    return isolate_code(gen(model, prompt, sys_prompt), "python")


def gpt_gen_bad_code(model, alg):
    sys_prompt = "Write a piece of code that has no comments, several errors, is difficult to read and extremely confusing."
    prompt = (
        "Return Python code that provides an implementation of "
        + alg
        + " that compiles correctly but does not accomplish the task of correctly sorting the input in one function"
    )
    # need to fix this
    prompt += f" defined as \n def {alg.lower()}:"
    return isolate_code(gen(model, prompt, sys_prompt), "python")


# Need to address multiple files of output...
def gpt_state_extraction(code_snip, input, title, model):
    # OK pausing on json_schema

    prompt1 = (
        "Given this piece of code, return a JSON list of elements that represent the state of variables that have been declared after each line of the code when run on the input"
        + str(input)
        + " ."
    )

    prompt2 = (
        """For example, the file 'FileOne.py' with code

        i = 3;
        #For Loop
        arr = [3, 1]
        for j in range(len(arr)):
            i ++

        Should yield the output of the json file Test"""
        + title
        + """.json

        [
            {
                "line number": 1,
                "variables": {"i": "3"}, 
                "file": FileOne
            },
            {
                "line number": 3,
                "variables": {"i": "3", "arr": "[3, 1]"}, 
                "file": FileOne
            },
            {
                "line number": 4,
                "variables": {"i": "3", "arr": "[3, 1]", "j": "0"}, 
                "file": FileOne
            }
            {
                "line number": 5,
                "variables": {"i": "4", "arr": "[3, 1]", "j": "0"}, 
                "file": FileOne
            },
            {
                "line number": 4,
                "variables": {"i": "4", "arr": "[3, 1]", "j": "1"}, 
                "file": FileOne
            },
                "line number": 5,
                "variables": {"i": "5", "arr": "[3, 1]", "j": "1"}, 
                "file": FileOne
            }
        ]

        """
    )

    prompt = prompt1 + "\n" + code_snip + "\n" + prompt2

    sys_prompt = "You are like a debugger in that you do not write code, but you can track the line-by-line variable states of code."

    messages = model.create_message(prompt, sys_prompt)

    # Given that I am asking llama!
    response = ""

    if (
        model.model == "Meta-Llama-3.1-70B-Instruct-Turbo"
        or model.model == "Meta-Llama-3.1-8B-Instruct-Turbo"
    ):
        try:
            print(StateExtractionFormat.model_json_schema())
            response = model.generate_json(
                messages, StateExtractionFormat.model_json_schema()
            )
            print("Response: ", response)
        except Exception as e:
            print(f"JSON .generation failed with this error: {e}")
    else:
        # print("Exception!")
        # raise Exception("This model's json generation is not implemented yet!")
        response = model.generate_text(messages)

    print(response)
    response = isolate_code(response, "json")

    #response = json.dumps(response)
    return response


def case_insensitive_split(text_to_split, split_str):
    split_text = []
    last_ind = 0
    for start_ind in range(len(text_to_split)):
        if text_to_split[start_ind : start_ind + len(split_str)].lower() == split_str.lower():
            split_text.append(text_to_split[last_ind:start_ind])
            last_ind = start_ind + len(split_str)
    return split_text


def isolate_code(only_code, string_ext):
    print(only_code)
    string_to_remove = "```" + string_ext
    ind = str.index(only_code, string_to_remove)
    if ind != -1:
        only_code = only_code[ind + len(string_to_remove) :]
    string_to_remove = "```"

    ind = str.index(only_code, string_to_remove)
    if ind != -1:
        only_code = only_code[:ind]

    return only_code


def save_code_to_file(file_path, gen_func, **args):

    if os.path.isfile(f"{file_path}"):
        with open(f"{file_path}", "r") as f:
            only_code = f.read()
    else:
        only_code = gen_func(**args)
        print(only_code)

        os.makedirs("/".join(file_path.split("/")[:-1]), exist_ok=True)
        with open(f"{file_path}", "w") as f:
            f.write(only_code.strip())

    return only_code


if __name__ == "__main__":
    # model = GPTModel();
    # Generate code!

    code_gen = ["QuickSort"]
    file_path = "llm_tests"
    files = []
    model = TogetherModel()

    for c in code_gen:

        files.append(f"{file_path}/code/{c}.py")

        code = save_code_to_file(
            f"{file_path}/code/{c}.py", gpt_gen_code, model=model, alg=c
        )
        print(code)

        # note: this code still does not work because of the model's failure...
        badcode = save_code_to_file(
            f"{file_path}/badcode/{c}.py", gpt_gen_bad_code, model=model, alg=c
        )
        # Uhh. so the only issue in this code: return quicksort(right) + [pivot] + quicksort(left) is that it's wrong.

        unittest = save_code_to_file(
            f"{file_path}/test/{c}test.py",
            gpt_gen_unit_test,
            model=model,
            code=code,
            alg=c,
        )
        print(unittest)

        # need to go through every test in the unit tests and then run this on each of them. this will also fix up the input.
        # problem: this is hardcoding for arrays
        unittests = case_insensitive_split(unittest, f"{c}(")
        tests = []
        for i in range(len(unittests)):
            nextStr = unittests[i].split(")")[0]
            if nextStr[0] == "[" and nextStr[-1] == "]":
                # notably it doesn't have to be evaluated as an array! I can just pass it in as a string since I'm using it as a string when feeding to gpt
                tests.append(eval(nextStr))
        print(tests)

        testNames = []
        unittestNames = unittest.split("def ")
        for i in range(1, len(unittestNames)):
            testNames.append(unittestNames[i].split("(self):")[0])
        print(testNames)

        # ok, taking a break re: varStates because for some reason generating JSON fails.
        # It looks like gpt_state_extraction
        for t, tName in zip(tests, testNames):
            if len(t) > 0:
                # note: t is just the name of the test, not the name of the PATH to the test.
                varStates = save_code_to_file(
                    f"{file_path}/state_output_logs/Test{c}.{tName}.json",
                    gpt_state_extraction,
                    code_snip=code,
                    input=t,
                    title=c,
                    model=model,
                )
                print(varStates)

        # things to do:
        # JSON extraction is not working at all. maybe just do generate text
        # another update to error: none of the code generation is working at all! <- only re: turbo, maybe the api key doesn't work w llama instruct turbo

        # done - make a new folder, put in the gpt code, and then run the subprocess of calling runtests on the new created file

        # figure out comparisons of files from actual state extraction

    # with open("llm_tests/tests.py", 'a') as f:
    #     for c in codeGen:
    #         with open(f'{file_path}/test/{c}test.py', 'r') as f2:
    #             f.write(f2.read())
    #             f.write('\n')

    # ModuleNotFoundError: No module named 'code.QuickSort'; 'code' is not a package
    # can't be fixed with new __init__ file

    success = False
    try:
        result = subprocess.run(
            ["python", "run_functions.py", file_path, "state_output_logs, test"],
            check=True,
            text=True,
        )
        # should generate the files!
        print("Test results:\n", result.stdout)
        success = True
    except Exception as e:
        print(e)
    # except subprocess.CalledProcessError as e:
    #     print("An error occurred while running tests:\n", e.stderr)
