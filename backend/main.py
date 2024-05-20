from flask import Flask, request, jsonify, send_from_directory
from llm_agents.gpt_agent import GPTAgent
from llm_agents.llava_phi_3_mini import LLavaPhi3MiniAgent
from llm_agents.llava_15_7b import Llava157B
from llm_agents.llava_3_8b import Llava38b
from dotenv import load_dotenv
from numba import cuda
import os
import gc

current_agent = GPTAgent()

app = Flask(__name__, static_folder='../front-end')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

load_dotenv()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def server_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    if not os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, 'index.html')
    return send_from_directory(app.static_folder, path)


@app.route('/agent', methods=['GET'])
def get_agent():
    return jsonify({'agent': current_agent.name()})


@app.route('/agent', methods=['POST'])
def set_agent():
    global current_agent
    agent = request.json['agent'].lower()
    
    if agent == current_agent.name():
        return jsonify({'agent': current_agent.name()})

    # Free up GPU memory before loading new agent
    del current_agent
    gc.collect()
    device = cuda.get_current_device()
    device.reset()

    match agent:
        case 'gpt':
            current_agent = GPTAgent()
        case 'llava-phi-3-mini':
            current_agent = LLavaPhi3MiniAgent()
        case 'llava-15-7b':
            current_agent = Llava157B()
        case 'llava-3-8b':
            current_agent = Llava38b()
        case _:
            return jsonify({'error': 'Invalid agent'})

    return jsonify({'agent': current_agent.name()})


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        print('File uploaded successfully')
    else:
        return jsonify({'error': 'Invalid file format'})

    response = current_agent.determine_region(file_path)
    print(response)
    return jsonify({'message': response})


if __name__ == '__main__':
    app.run(debug=False, port=8080)

