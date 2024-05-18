from flask import Flask, request, jsonify, send_from_directory
from llm_agents.gpt_agent import GPTAgent
from llm_agents.llava_phi_3_mini import LLavaPhi3MiniAgent
from dotenv import load_dotenv
import os
import torch

current_agent = LLavaPhi3MiniAgent()

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
    agent = request.json['agent'].lower()
    
    if agent == current_agent.name():
        return jsonify({'agent': current_agent.name()})

    # Free up GPU memory before loading new agent
    global current_agent
    del current_agent
    torch.cuda.empty_cache()

    if agent == 'gpt':
        current_agent = GPTAgent()
    elif agent == 'llava-phi-3-mini':
        current_agent = LLavaPhi3MiniAgent()
    else:
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
