import os
from typing import List
#from openai import OpenAI
import openai 
import together
from together import Together

#need to make a superclass

class BaseModel:
    def __init__(self, model):
        self.model = model
    
    def generate_text(self, messages, params):
        pass

    def create_message(self, prompt, systemPrompt="") -> List:
        messages = []
        if len(systemPrompt) > 0:
            messages.append({
                "role": "system",
                "content": systemPrompt
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        return messages
    


class TogetherModel(BaseModel):
    def __init__(self, model='Meta-Llama-3.1-70B-Instruct'):
        #might need turbo at the end for json mode
        # meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
        super().__init__(model)
        self.client = Together(
            api_key = os.environ.get("SAMBANOVA_API_KEY"),
            base_url = "https://api.sambanova.ai/v1"
        )

    def generate_text(self, messages, params = {"temperature": 0.1, "top_p": 0.1}) -> str:
        print(params)
        try:
            print(params)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **params
            )

            print(response)
            return response.choices[0].message.content
        
        except Exception as e:
            print("Error generating text: ", e)
            return ""
        
            
    def generate_json(self, messages, schema, params = {"temperature": 0.1, "top_p": 0.1}):
        params = params.copy()
        params['response_format'] = {
            "type": "json_object",
            "schema": schema
        }
        # params['response_format'] = "json_object"
        # params['schema'] = schema
        return self.generate_text(messages, params)

# t = TogetherModel()
# print(t.generate_text(t.create_message("Hi!")))
# Yay! This works! :)

class GPTModel(BaseModel):
    def __init__(self, model='Meta-Llama-3.1-70B-Instruct'):
                 #model="gpt-4o-mini-2024-07-18"):
        super().__init__(model)
        self.client = openai.OpenAI(
            api_key = os.environ.get("SAMBANOVA_API_KEY"),
            base_url = "https://api.sambanova.ai/v1"
        )

    def generate_text(self, messages, params = {"temperature": 0.1, "top_p": 0.1}) -> str:
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                **params
            )
    
            text_response = response.choices[0].message.parsed

            return text_response
    
        except Exception as e:
            print("Error generating text: ", e)
            return ""

    def generate_json_gpt(self, messages, params = {"temperature": 0.1, "top_p": 0.1}) -> str:
        if self.model in ['gpt-4o-mini', 'gpt-4o-2024-08-06']:
            params['response_format'] = {
                "type": "json_schema",
                "json_schema": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "steps": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "line number": {
                                            "type": "string"
                                            },
                                        "variables": {
                                                "type": "object"  
                                            }
                                    },
                                }
                            },
                        },
                    },
                }
            }
        else:
            params['response_format'] = { "type": "json_object" }

        return self.generate_text(messages, params)
