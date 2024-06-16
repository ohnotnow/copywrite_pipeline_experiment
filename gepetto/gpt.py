import os
import json
from enum import Enum
from openai import OpenAI
from gepetto.response import ChatResponse, FunctionResponse

class Model(Enum):
    GPT4_32k = ('gpt-4-32k', 0.03, 0.06)
    GPT_4_1106_PREVIEW = ('gpt-4-1106-preview', 0.01, 0.03)
    GPT_4_TURBO = ('gpt-4-turbo', 0.01, 0.03)
    GPT_4_OMNI = ('gpt-4o', 0.005, 0.015)
    GPT4 = ('gpt-4', 0.06, 0.12)
    GPT3_5_Turbo_gpt_1106 = ('gpt-3.5-turbo-1106', 0.001, 0.002)
    GPT3_5_Turbo_16k = ('gpt-3.5-turbo-16k', 0.003, 0.004)
    GPT3_5_Turbo = ('gpt-3.5-turbo', 0.0015, 0.002)

class GPTModel():
    name = "Gepetto"
    def get_token_price(self, token_count, direction="output", model_engine="gpt-4o"):
        token_price_input = 0
        token_price_output = 0
        for model in Model:
            if model_engine.startswith(model.value[0]):
                token_price_input = model.value[1] / 1000
                token_price_output = model.value[2] / 1000
                break
        if direction == "input":
            return round(token_price_input * token_count, 4)
        return round(token_price_output * token_count, 4)

    async def chat(self, messages, temperature=1.8, model="gpt-4o", top_p=0.6):
        """Chat with the model.

        Args:
            messages (list): The messages to send to the model.
            temperature (float): The temperature to use for the model.

        Returns:
            str: The response from the model.
            tokens: The number of tokens used.
            cost: The estimated cost of the request.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = "https://api.openai.com/v1/"
        client = OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
        )
        # print(str(response.choices[0].message))
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        tokens = input_tokens + output_tokens
        output_cost = self.get_token_price(output_tokens, "output", model)
        input_cost = self.get_token_price(input_tokens, "input", model)
        cost = input_cost + output_cost
        message = str(response.choices[0].message.content)
        return ChatResponse(message, tokens, cost, model)

    async def function_call(self, messages = [], tools = [], temperature=0.7, model="gpt-4o"):
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = "https://api.openai.com/v1/"
        client = OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": tools[0]["function"]["name"]}},
        )
        # print(str(response.choices[0].message))
        tokens = response.usage.total_tokens
        cost = self.get_token_price(tokens, "output", model)
        message = response.choices[0].message
        parameters = json.loads(message.tool_calls[0].function.arguments)
        return FunctionResponse(parameters, tokens, cost)

class GPTModelSync():
    name = "Gepetto"
    def get_token_price(self, token_count, direction="output", model_engine="gpt-4o"):
        token_price_input = 0
        token_price_output = 0
        for model in Model:
            if model_engine.startswith(model.value[0]):
                token_price_input = model.value[1] / 1000
                token_price_output = model.value[2] / 1000
                break
        if direction == "input":
            return round(token_price_input * token_count, 4)
        return round(token_price_output * token_count, 4)

    def chat(self, messages, temperature=1.0, model="gpt-4o", top_p=1.0):
        """Chat with the model.

        Args:
            messages (list): The messages to send to the model.
            temperature (float): The temperature to use for the model.

        Returns:
            str: The response from the model.
            tokens: The number of tokens used.
            cost: The estimated cost of the request.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = "https://api.openai.com/v1/"
        client = OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
        )
        # print(str(response.choices[0].message))
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        tokens = input_tokens + output_tokens
        output_cost = self.get_token_price(output_tokens, "output", model)
        input_cost = self.get_token_price(input_tokens, "input", model)
        cost = input_cost + output_cost
        message = str(response.choices[0].message.content)
        return ChatResponse(message, tokens, cost, model)

    def function_call(self, messages = [], tools = [], temperature=0.7, model="gpt-4o"):
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = "https://api.openai.com/v1/"
        client = OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": tools[0]["function"]["name"]}},
        )
        # print(str(response.choices[0].message))
        tokens = response.usage.total_tokens
        cost = self.get_token_price(tokens, "output", model)
        message = response.choices[0].message
        parameters = json.loads(message.tool_calls[0].function.arguments)
        return FunctionResponse(parameters, tokens, cost)
