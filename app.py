from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import os
import base64

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Directory to save captured images
SAVE_DIR = "../FRT_Recognition/known_faces"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_next_filename(directory, name):
    """
    Generates the next filename in sequence for the given name.
    Example: If 'name_0001.jpg' exists, it returns 'name_0002.jpg'.
    """
    counter = 1
    while True:
        file_name = f"{name}_{counter:04d}.jpg"
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            return file_path
        counter += 1

@app.route('/capture', methods=['POST'])
@cross_origin(origins=['http://localhost:3000'])
def capture_image():
    data = request.json
    if not data or 'name' not in data or 'image' not in data:
        return jsonify({"error": "Name and image data are required"}), 400
    
    name = data['name']
    image_data = data['image']
    
    # Create a directory with the name provided
    user_dir = os.path.join(SAVE_DIR, name)
    os.makedirs(user_dir, exist_ok=True)
    
    # Generate the next file name
    file_path = get_next_filename(user_dir, name)
    
    # Decode the base64 image and save it
    with open(file_path, "wb") as file:
        file.write(base64.b64decode(image_data.split(",")[1]))  # Strip off data:image/jpeg;base64,
    
    return jsonify({"message": f"Image saved at {file_path}"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
