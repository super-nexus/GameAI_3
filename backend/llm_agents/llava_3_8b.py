from llm_agents.base_llama_agent import BaseLlamaAgent    
from llama_cpp.llama_chat_format import Llava15ChatHandler


class Llava38b(BaseLlamaAgent):
    def __init__(self):
        mmproj_path = "mnt/media-share/models/llava-llama-3-8b-mmproj.gguf"
        model_path = "mnt/media-share/models/llava-llama-3-8b.gguf"
        chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)
        super().__init__(model_path, 15, chat_handler)

    def name(self):
        return "llava-3-8b"
