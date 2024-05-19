from llm_agents.base_llama_agent import BaseLlamaAgent    
from llama_cpp.llama_chat_format import Llava15ChatHandler


class Llava157B(BaseLlamaAgent):
    def __init__(self):
        mmproj_path = "models/llava-15-7b-mmproj.gguf"
        model_path = "models/llava-15-7b.gguf"
        chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)
        super().__init__(model_path, -1, chat_handler)

    def name(self):
        return "llava-15-7b"
