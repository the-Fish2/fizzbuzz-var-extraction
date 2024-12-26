from llm_interface.gpt_model import GPTModel #type:ignore
import subprocess
import os
import json
from llm_interface.state_extraction import StateExtractionFormat #type:ignore

def gen(model, prompt, sprompt):
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
    sprompt = "Write a piece of code that represents the skill of an intelligent but somewhat misguided coder."
    prompt = "Return only Python code that provides an implementation of " + alg + " that compiles correctly but does not accomplish the task of correctly sorting the input." 
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

        Should yield the output of the jsonl file Test""" + title + """.jsonl

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
    if (model.model == 'Meta-Llama-3.1-70B-Instruct'): 
        response = model.generate_text(messages, StateExtractionFormat.model_json_schema())
        print(response)
    else:
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
    model = GPTModel();

    for c in codeGen:
            
        files.append(f'{filesPath}/code/{c}.py')

        code = saveCodeToFile(f'{filesPath}/code/{c}.py', gptGenCode, model=model, alg=c)
        print(code)

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
        
        for t, tName in zip(tests[3:4], testNames[3:4]):
            if (len(t) > 0):
                #note: t is just the name of the test, not the name of the PATH to the test. 
                varStates = saveCodeToFile(f'{filesPath}/state_output_logs/{c}.{tName}.jsonl', gptStateExtraction, codeSnip=code, input=t, title=c, model=model)
                print(varStates)

        
        #things to do:
        #implement bad code gen and see if it can still track the code
        #figure out comparisons of files from actual state extraction
        #make a new folder, put in the gpt code, and then run the subprocess of calling runtests on the new created file
        #also need to automatically generate additional sample test cases on each of these
        #then compare that runtest file to the varExtraction code here


    # success = False
    # try:
    #     result = subprocess.run(["python", "run_functions.py", filesPath], check=True, capture_output=True, text=True)
    #     #should generate the files!
    #     print("Test results:\n", result.stdout)
    #     success = True
    # except subprocess.CalledProcessError as e:
    #     print("An error occurred while running tests:\n", e.stderr)

    # print(gptCode)
    
    # input = [1, 2, 3, 4, 5]
    # with open('algorithm_tests/test2.py', 'r') as f:
    #     code = f.read()
    #     gptCode = code

    # print(code)
    
    #varExtraction = gptCodeExtraction(model, input, gptCode);

    # msgs = model.create_message("Hello! Please give me a JSON array of three possible responses you could give me. ")
    # response = model.generate_json(msgs)
    # print(response)