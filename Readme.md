# GeoGuessr AI

## How to run?

1. Clone the repo
2. Run `pip install -r backend/requirements.txt`

### For GPT-4o model

You need to create an OPENAI_API_KEY env variable. 
For this you will need to create an openai account top up your balance

### For llava-llama models

For these models you will need to have an NVIDIA GPU with 24GB of onboard memory (RTX-3090). 
If you do not have that locally you can rent a machine on [vast.ai](https://vast.ai/) for around 30 cents
per hour.

In order to interact with the GPU nvidia's cuda library is needed, follow [this guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
to install it.

Afterwards, you will need to install `llama-cpp-python`.
Run the following command `CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python`.

Finally, you will need to download the models and place them within `backend/models` directory

* [Llava-3-8B](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/llava-llama-3-8b-v1_1-f16.gguf?download=true)
* [Llava-3-8B-mmproj](https://huggingface.co/xtuner/llava-llama-3-8b-v1_1-gguf/resolve/main/llava-llama-3-8b-v1_1-mmproj-f16.gguf?download=true)
* [Llava-1.5-7B](https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q5_k.gguf?download=true)
* [Llava-1.5-7B-mmproj](https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/mmproj-model-f16.gguf?download=true)

