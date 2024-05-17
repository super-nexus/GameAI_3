from flask import Flask, request, jsonify, send_from_directory
from llm_agents.gpt_agent import GPTAgent
from llm_agents.llava_phi_3_mini import LLavaPhi3MiniAgent
from dotenv import load_dotenv
import os


app = Flask(__name__, static_folder='../front-end')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

load_dotenv()
current_agent = LLavaPhi3MiniAgent()

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
    app.run(debug=True, port=5000)
