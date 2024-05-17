from transformers import pipeline
from PIL import Image    
from base_llm_agent import BaseLLMAgent
import requests


class LLavaPhi3MiniAgent(BaseLLMAgent):
    def __init__(self):
        self.model_id = "xtuner/llava-phi-3-mini-hf"
        self.pipe = pipeline("image-to-text", model=self.model_id, device='cuda')
        self.prompt = "<|user|>\n<image>\nWhere do you think the following image is located, return the response as a json with two keys, first key is the country where you specify which country do you think is depicted in the picture, second key is the region where you specify whether you think that is east, west, north, south or central part of that country.<|end|>\n<|assistant|>\n"

    def name(self):
        return "llava-phi-3-mini"

    def determine_region(self, image_path):
        image = Image.open(image_path)
        outputs = pipe(image, prompt=self.prompt, generate_kwargs={"max_new_tokens": 200})
        print(outputs)
        return outputs[0]['generated_text']


