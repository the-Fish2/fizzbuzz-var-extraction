import os
from typing import List
#from openai import OpenAI
import openai

class GPTModel:
    def __init__(self, model='Meta-Llama-3.1-70B-Instruct'):
                 #model="gpt-4o-mini-2024-07-18"):
        self.model = model
        self.client = openai.OpenAI(
            api_key = os.environ.get("SAMBANOVA_API_KEY"),
            base_url = "https://api.sambanova.ai/v1"
        )

    def generate_text(self, messages, params = {"temperature": 0.1, "top_p": 0.1}) -> str:
        try:
            response = self.client.chat.completions.create(
            #self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                **params
            )
    
            #text_response = response.choices[0].message.parsed

            #return text_response

            # response = self.client.chat.completions.create(
            #     model='Meta-Llama-3.1-70B-Instruct',
            #     messages=messages,
            #     **params
            # )

            return response.choices[0].message.content
    
        except Exception as e:
            print("Error generating text: ", e)
            return ""
        
    def generate_json(self, messages, params = {"temperature": 0.1, "top_p": 0.1}) -> str:
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

    
    def create_message(self, prompt, systemPrompt = "") -> List:
        messages = []

        if len(systemPrompt) > 0:
            messages.append({
                "role":"system",
                "content": systemPrompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })
        return messages;