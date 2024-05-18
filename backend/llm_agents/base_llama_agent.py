from llm_agents.base_llm_agent import BaseLLMAgent
from llama_cpp import Llama
import base64
import json

class BaseLlamaAgent(BaseLLMAgent):

    def __init__(self, model_path, num_gpu_layers, chat_handler):
        self.model_path = model_path
        self.num_gpu_layers = num_gpu_layers
        self.chat_handler = chat_handler
        self.llm = Llama(
            model_path=self.model_path,
            chat_handler=self.chat_handler,
            n_ctx=2048,
            n_gpu_layers=self.num_gpu_layers
        )

    def determine_region(self, image_path):
        image_base64 = load_image_as_base64(image_path)
        response = self.llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert GeoGuessr player that returns the location of the image in a JSON format",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Where do you think this image was taken, give me the country and the region of the country (north, east, west, south, central)"},
                        {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"},
                    ],
                },
            ],
            response_format={
                "type": "json_object",
                "schema": {
                    "type": "object",
                    "properties": {
                        "country": {"type": "string"},
                        "region": {"type": "string"},
                    },
                    "required": ["country", "region"],
                },
            },
            temperature=0.3,
        )

        return json.loads(response['choices'][0]['message']['content'])



def load_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

