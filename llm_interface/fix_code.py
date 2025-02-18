from llm_interface.gpt_model import GPTModel, TogetherModel
from llm_interface.generate_tests import gen, isolate_code
import subprocess
import os
import json

""" 
This file is unfinished as of yet, but will hopefully soon contain the prompt for running llama on swe-bench given the state extraction of the code base
"""


def gpt_fix_bad_code(model, code: str):
    sys_prompt = "You are a computer programmer that is good at fixing code in a minimal and clean way to make code functional and correct. "
    prompt = (
        "Return Python code that fixes the code here to ensure it's functionality"
        + str(code)
    )
    return isolate_code(gen(model, prompt, sys_prompt), "python")
