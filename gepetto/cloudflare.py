import os
import requests
from gepetto.response import ChatResponse, FunctionResponse

class ClodflareModel():
    name = "RecipeThis"
    def get_token_price(self, token_count, direction="output", model_engine="mistralai/Mistral-7B-Instruct-v0.1"):
        return 0

    async def chat(self, messages, temperature=1.0, model="@cf/meta/llama-2-7b-chat-int8"):
        """Chat with the model.

        Args:
            messages (list): The messages to send to the model.
            temperature (float): The temperature to use for the model.

        Returns:
            ChatResponse: The response from the model.
        """
        input = { "messages": messages }
        API_KEY=os.getenv('CLOUDFLARE_API_KEY')
        API_BASE_URL = os.getenv('CLOUDFLARE_API_BASE')
        headers = {"Authorization": f"Bearer {API_KEY}"}
        s = requests.Session()
        message = ""
        with s.post(f"{API_BASE_URL}{model}", headers=headers, json=input, stream=True) as stream:
            for word in stream.iter_lines():
                message += word.decode('utf-8')
        return ChatResponse(message, 0, 0, model)

    async def function_call(self, messages = [], tools = [], temperature=0.7, model="mistralai/Mistral-7B-Instruct-v0.1"):
        return FunctionResponse({"error": "Cannot run functions"}, 0, 0)
