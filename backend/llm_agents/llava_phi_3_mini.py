from llm_agents.base_llama_agent import BaseLlamaAgent    
from llama_cpp.llama_chat_format import Llava15ChatHandler


class LLavaPhi3MiniAgent(BaseLlamaAgent):
    def __init__(self):
        mmproj_path = "models/llava-phi-3-mini-mmproj-f16.gguf"
        model_path = "models/llava-phi-3-mini.gguf"
        chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)
        super().__init__(model_path, 28, chat_handler)

    def name(self):
        return "llava-phi-3-mini"
