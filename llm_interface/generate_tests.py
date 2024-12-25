from llm_interface.gpt_model import GPTModel #type:ignore
import subprocess

def gen(model, prompt, sprompt):
    messages = model.create_message(prompt, sprompt)
    response = model.generate_text(messages)
    return response

def gptGenCode(model, alg):
    sprompt = "Write only a piece of code with no text that represents the skill of an intermediate coder."
    prompt = "Return only Python code that provides a working implementation of " + alg
    return gen(model, prompt, sprompt)

def gptGenUnitTest(model, code, alg):
    sprompt = "Write only a piece of code with no text."
    prompt = "Please write several unit tests for this code in one testcase " + code + " in the following format: "
    prompt += f""" 
        class Test{alg}(unittest.TestCase):
            def test_1:
                #test 1
            def test_2:
                #test_2

        and so forth.
        """
    return gen(model, prompt, sprompt)


def gptGenBadCode(model, alg):
    sprompt = "Write a piece of code that represents the skill of an intelligent but somewhat misguided coder."
    prompt = "Return only Python code that provides an implementation of " + alg + " that compiles correctly but does not accomplish the task of correctly sorting the input." #need to fix this
    return gen(model, prompt, sprompt)


#Need to address multiple files of output...
def gptCodeExtraction(codeSnip, input, model):
    prompt1 = """
        Given this piece of code, return a json array of elements that represent the state of variables after each line of the code when run on the input 
        """ + input + " ."

    prompt2 = """
        For example, the file 'hello.py' with code

        i = 3;
        for j in range(1):
            i ++

        Should yield the output of the jsonl file Test""" + input + """.jsonl

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

        """
    
    prompt = prompt1 + "\n" + codeSnip + "\n" + prompt2;

    return gen(model, prompt, "You are a helpful code tracker that can identify varying code states.")

    #make a new folder, put in the gpt code, and then run the subprocess of calling runtests on the new created file
    #also need to automatically generate additional sample test cases on each of these
    #then compare that runtest file to the varExtraction code here


if __name__ == "__main__":
    #model = GPTModel();

    #Generate code!

    codeGen = ["QuickSort"]
    filesPath = "llm_tests"
    files = []
    model = GPTModel();
    for c in codeGen:
        gptCode = gptGenCode(model, c)
        with open(f'{filesPath}/code/{c}.py', 'w') as f:
            f.write(gptCode)

        gptUnitTest = gptGenUnitTest(model, gptCode, c)
        with open(f'{filesPath}/test/{c}test.py', 'w') as f:
            f.write(gptUnitTest)
            files.append(f'{filesPath}/{c}.py')

        varStateExtraction = gptCodeExtraction(gptCode, c, model)
    
        with open(f'{filesPath}/state_output_logs/{c}.jsonl', 'w') as f:
            f.write(varStateExtraction)

    success = False
    try:
        result = subprocess.run(["python", "run_functions.py", filesPath], check=True, capture_output=True, text=True)
        #should generate the files!
        print("Test results:\n", result.stdout)
        success = True
    except subprocess.CalledProcessError as e:
        print("An error occurred while running tests:\n", e.stderr)

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