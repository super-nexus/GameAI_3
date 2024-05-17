from langchain_openai import ChatOpenAI
from langchain.chains import TransformChain
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from llm_agents.base_llm_agent import BaseLLMAgent
import base64
import os


class ImageInformation(BaseModel):
    """Information about an image."""
    image_description: str = Field(description="a short description of the image")
    country: str = Field(description="The country where the image was taken")
    region: str = Field(description="Part of the country where the image was taken, it can be north, south, east, west or central")


class GPTAgent(BaseLLMAgent):

    def __init__(self):
        # OPENAI_API_KEY env variable must be set
        self.load_image_chain = TransformChain(
            input_variables=["image_path"],
            output_variables=["image"],
            transform=self.load_image
        )

    def name(self) -> str:
        return "gpt"
    
    def load_image(self, inputs: dict) -> dict:
        """Load image from file and encode it as base64."""
        image_path = inputs["image_path"]
    
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        image_base64 = encode_image(image_path)
        return {"image": image_base64}

    def determine_region(self, image_path: str) -> dict:
        print(f"Image path: {image_path}")
        vision_prompt = """
        Given the image, provide the following information:
        - The country where the image was taken
        - The part of the country where the image was taken (north, south, east, west, central)
        - A short description of why you think the image was taken in that country
        """
        vision_chain = self.load_image_chain | image_model | parser
        return vision_chain.invoke({'image_path': f'{image_path}', 
                               'prompt': vision_prompt})


parser = JsonOutputParser(pydantic_object=ImageInformation)

@chain
def image_model(inputs: dict) -> str | list[str] | dict:
     """Invoke model with image and prompt."""
     model = ChatOpenAI(temperature=0.5, model="gpt-4-vision-preview", max_tokens=1024)
     system_message = SystemMessage("You are an expert geoguessr player and you are trying to estimate the location of the image.")
     human_message = HumanMessage(
         content=[
             {"type": "text", "text": inputs["prompt"]},
             {"type": "text", "text": parser.get_format_instructions()},
             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}}
         ]
     )


     msg = model.invoke([system_message, human_message])
     return msg.content


