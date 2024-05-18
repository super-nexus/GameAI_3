from transformers import pipeline
from PIL import Image    
from llm_agents.base_llm_agent import BaseLLMAgent

class BaseHFAgent(BaseLLMAgent):

    def __init__(self, model_id):
        self.model_id = model_id
        self.pipe = pipeline("image-to-text", model=self.model_id, device='cuda')
        self.prompt = "<|user|>\n<image>\nWhere do you think the following image is located, return the response as a json with two keys, first key is the country (all lowercase) where you specify which country do you think is depicted in the picture, second key is the region (all lowercase) where you specify whether you think that is east, west, north, south or central part of that country.<|end|>\n<|assistant|>\n"

    def determine_region(self, image_path):
        image = Image.open(image_path)
        outputs = self.pipe(image, prompt=self.prompt, generate_kwargs={"max_new_tokens": 200})
        print(outputs)
        return outputs[0]['generated_text']
