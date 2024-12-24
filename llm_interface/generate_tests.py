from llm_interface.gpt_model import GPTModel #type:ignore

def gptGenCode(model, alg):
    sprompt = "Write a piece of code that represents the skill of an intermediate coder."
    prompt = "Return code that provides a working implementation of " + alg
    messages = model.create_message(prompt, sprompt)
    response = model.generate_text(messages)
    return response

def gptCodeExtraction(codeSnip, model):
    prompt1 = """
        Given this piece of code, return a json array of elements that represent the state of variables after each line of the code. 
        """

    prompt2 = """
        For example, 

        i = 3;
        for j in range(1):
            i ++

        Should yield the output

        [
            {
                'line number': 1,
                'variables': {'i': '3'} 
            },
            {
                'line number': 2,
                'variables': {'i': '3', 'j': '0'} 
            }
            {
                'line number': 3,
                'variables': {'i': '4', 'j': '0'} 
            },
            {
                'line number': 2,
                'variables': {'i': '4', 'j': '1'} 
            },
                'line number': 3,
                'variables': {'i': '5', 'j': '1'} 
            },
        ]

        """
    
    prompt = prompt1 + "\n" + codeSnip + "\n" + prompt2;
    messages = model.create_message(prompt)
    response = model.generate_json(messages)

    print(response)

def pipelineStateComp():
    model = GPTModel();
    gptCode = gptGenCode(model, "QuickSort")
    print(gptCode)
    varExtraction = gptCodeExtraction(model, gptCode)

    #make a new folder, put in the gpt code, and then run the subprocess of calling runtests on the new created file
    #then compare that runtest file to the varExtraction code here