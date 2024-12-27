from llm_interface.gpt_model import GPTModel, TogetherModel
import subprocess
import os
import json
from llm_interface.state_extraction import StateExtractionFormat

def gen(model, prompt, sprompt=""):
    messages = model.create_message(prompt, sprompt)
    response = model.generate_text(messages)
    return response

def gptGenCode(model, alg):
    sprompt = "Write only a piece of code with no text that represents the skill of an intermediate coder."
    prompt = "Return only Python code that provides a working implementation of " + alg
    prompt += f" defined as \n def {alg.lower()}:"
    #assuming this is def alg (in all lowercase)
    return isolateCode(gen(model, prompt, sprompt))

def gptGenUnitTest(model, code, alg):
    sprompt = "Write only a piece of code with no text."
    prompt = "Please write several unit tests for this code in one testcase " + code + " in the following format: "
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
    return isolateCode(gen(model, prompt, sprompt))


def gptGenBadCode(model, alg):
    sprompt = "Write a piece of code that has no comments, several errors, is difficult to read and extremely confusing."
    prompt = "Return Python code that provides an implementation of " + alg + " that compiles correctly but does not accomplish the task of correctly sorting the input in one function" 
    #need to fix this
    prompt += f" defined as \n def {alg.lower()}:"
    return isolateCode(gen(model, prompt, sprompt))


#Need to address multiple files of output...
def gptStateExtraction(codeSnip, input, title, model):

    prompt1 = "Given this piece of code, return a json array of elements that represent the state of variables after each line of the code when run on the input" + str(input) + " ."

    prompt2 = '''For example, the file 'hello.py' with code

        i = 3;
        for j in range(1):
            i ++

        Should yield the output of the json file Test''' + title + '''.json

        [
            {
                'line number': 1,
                'variables': {'i': '3'}, 
                'file': hello
            },
            {
                'line number': 2,
                'variables': {'i': '3', 'j': '0'}, 
                'file': hello
            }
            {
                'line number': 3,
                'variables': {'i': '4', 'j': '0'}, 
                'file': hello
            },
            {
                'line number': 2,
                'variables': {'i': '4', 'j': '1'}, 
                'file': hello
            },
                'line number': 3,
                'variables': {'i': '5', 'j': '1'}, 
                'file': hello
            },
        ]

        '''
    
    prompt = prompt1 + "\n" + codeSnip + "\n" + prompt2;

    messages = model.create_message(prompt)

    #Given that I am asking llama!
    response = "" 

    if (model.model == 'Meta-Llama-3.1-70B-Instruct-Turbo' or model.model == 'Meta-Llama-3.1-8B-Instruct-Turbo'): 
        try:
            print( StateExtractionFormat.model_json_schema())
            response = model.generate_json(messages, StateExtractionFormat.model_json_schema())
            print("Response: ", response)
        except Exception as e:
            print(f"JSON generation failed with this error: {e}")
    else:
        print("Exception!")
        raise Exception("This model's json generation is not implemented yet!")


    return response

def caseInsensitiveSplit(textToSplit, splitStr):
    splitText = []
    lastInd = 0
    for startInd in range(len(textToSplit)):
        if (textToSplit[startInd:startInd+len(splitStr)].lower() == splitStr.lower()):
            splitText.append(textToSplit[lastInd:startInd])
            lastInd = startInd+len(splitStr)
    return splitText

def isolateCode(onlyCode):
    print(onlyCode)
    stringToRemove = "```python"
    ind = str.index(onlyCode, stringToRemove)
    if ind != -1:
        onlyCode = onlyCode[ind+len(stringToRemove):]
    stringToRemove = "```"

    ind = str.index(onlyCode, stringToRemove)
    if ind != -1:
        onlyCode = onlyCode[:ind]

    return onlyCode

def saveCodeToFile(filePath, genFunc, **args):

    if (os.path.isfile(f'{filePath}')):
        with open(f'{filePath}', 'r') as f:
            onlyCode = f.read()
    else:

        onlyCode = genFunc(**args)
        print(onlyCode)

        os.makedirs('/'.join(filePath.split('/')[:-1]), exist_ok=True)
        with open(f'{filePath}', 'w') as f:
            f.write(onlyCode.strip())

    return onlyCode

if __name__ == "__main__":
    #model = GPTModel();
    #Generate code!

    codeGen = ["QuickSort"]
    filesPath = "llm_tests"
    files = []
    model = TogetherModel();

    for c in codeGen:
            
        files.append(f'{filesPath}/code/{c}.py')

        code = saveCodeToFile(f'{filesPath}/code/{c}.py', gptGenCode, model=model, alg=c)
        print(code)

        #note: this code still does not work because of the model's failure...
        badcode = saveCodeToFile(f'{filesPath}/badcode/{c}.py', gptGenBadCode, model=model, alg=c)
        #Uhh. so the only issue in this code: return quicksort(right) + [pivot] + quicksort(left) is that it's wrong. 

        unittest = saveCodeToFile(f'{filesPath}/test/{c}test.py', gptGenUnitTest, model=model, code=code, alg=c)
        print(unittest)

        #need to go through every test in the unit tests and then run this on each of them. this will also fix up the input. 
        #problem: this is hardcoding for arrays
        unittests = caseInsensitiveSplit(unittest, f'{c}(')
        tests = []
        for i in range(len(unittests)):
            nextStr = (unittests[i].split(')')[0])
            if nextStr[0] == '[' and nextStr[-1] == ']':
                #notably it doesn't have to be evaluated as an array! I can just pass it in as a string since I'm using it as a string when feeding to gpt
                tests.append(eval(nextStr))
        print(tests)

        testNames = []
        unittestNames = unittest.split('def ')
        for i in range (1, len(unittestNames)):
            testNames.append(unittestNames[i].split('(self):')[0])
        print(testNames)
        

        #ok, taking a break re: varStates because for some reason generating JSON fails. 
        for t, tName in zip(tests[3:4], testNames[3:4]):
            if (len(t) > 0):
                #note: t is just the name of the test, not the name of the PATH to the test. 
                varStates = saveCodeToFile(f'{filesPath}/state_output_logs/{c}.{tName}.json', gptStateExtraction, codeSnip=code, input=t, title=c, model=model)
                print(varStates)

        
        #things to do:
        #JSON extraction is not working at all. maybe just do generate text
        #another update to error: none of the code generation is working at all! <- only re: turbo, maybe the api key doesn't work w llama instruct turbo

        #done - make a new folder, put in the gpt code, and then run the subprocess of calling runtests on the new created file

        #figure out comparisons of files from actual state extraction

    # with open("llm_tests/tests.py", 'a') as f:
    #     for c in codeGen:
    #         with open(f'{filesPath}/test/{c}test.py', 'r') as f2:
    #             f.write(f2.read())
    #             f.write('\n')

    #ModuleNotFoundError: No module named 'code.QuickSort'; 'code' is not a package
    #can't be fixed with new __init__ file

    success = False
    try:
        result = subprocess.run(["python", "run_functions.py", filesPath, "state_output_logs, test"], check=True, capture_output=True, text=True)
        #should generate the files!
        print("Test results:\n", result.stdout)
        success = True
    except subprocess.CalledProcessError as e:
        print("An error occurred while running tests:\n", e.stderr)
