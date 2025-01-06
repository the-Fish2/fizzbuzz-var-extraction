import os
from typing import List, Dict, Any
import openai
import together
from together import Together


class BaseModel:
    def __init__(self, model: str):
        self.model = model

    def generate_text(self, messages: List, params={}):
        pass

    def create_message(self, prompt: str, system_prompt: str = "") -> List:
        messages = []
        if len(system_prompt) > 0:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return messages


class TogetherModel(BaseModel):
    """
    Model with TogetherAI
    """
    def __init__(
        self,
        model="Meta-Llama-3.1-70B-Instruct",
        curr_api_key=os.environ.get("SAMBANOVA_API_KEY"),
    ):
        # might need turbo at the end for json mode
        # meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
        super().__init__(model)
        self.client = openai.OpenAI(
            api_key=curr_api_key,
            base_url="https://api.sambanova.ai/v1",
        )

    def generate_text(self, messages: List, params: Dict={"temperature": 0.1, "top_p": 0.1}) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, **params
            )

            return response.choices[0].message.content if response is not None else ""

        except Exception as e:
            print("Error generating text: ", e)
            return ""

    def generate_json(
        self, messages: List, schema: Dict, params={"temperature": 0.1, "top_p": 0.1}
    ):
        #schema should be of form model_json_schema()
        params = params.copy()
        params["response_format"] = {"type": "json_object", "schema": schema}
        params["response_format"] = "json_object"
        params["schema"] = schema
        return self.generate_text(messages, params)


class GPTModel(BaseModel):
    """
    Model with OpenAI
    """
    def __init__(self, model="Meta-Llama-3.1-70B-Instruct"):
        # model="gpt-4o-mini-2024-07-18"):
        super().__init__(model)
        self.client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url="https://api.sambanova.ai/v1",
        )

    def generate_text(self, messages: List, params: Dict ={"temperature": 0.1, "top_p": 0.1}) -> str:
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model, messages=messages, **params
            )

            text_response = response.choices[0].message.parsed

            return text_response if text_response is not None else ""

        except Exception as e:
            print("Error generating text: ", e)
            return ""

    def generate_json_gpt(
        self, messages: List, params: Dict ={"temperature": 0.1, "top_p": 0.1}
    ) -> str:
        if self.model in ["gpt-4o-mini", "gpt-4o-2024-08-06"]:
            params["response_format"] = {
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
                                        "line number": {"type": "string"},
                                        "variables": {"type": "object"},
                                    },
                                },
                            },
                        },
                    },
                },
            }
        else:
            params["response_format"] = {"type": "json_object"}

        return self.generate_text(messages, params)
