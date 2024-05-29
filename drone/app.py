from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

def generate_annotation(image_path):
    # Local API endpoint running the LLaVA model
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llava:7b",
        "prompt": f"Describe this image: {image_path}",
        "images": [image_path]
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("message", {}).get("content", "No annotation available")
    else:
        return "Failed to get annotation"

@app.route('/annotate', methods=['POST'])
def annotate():
    if 'image_path' not in request.json:
        return jsonify({"error": "No image path provided"}), 400

    image_path = request.json['image_path']
    if not os.path.exists(image_path):
        return jsonify({"error": "Image file does not exist"}), 400

    annotation = generate_annotation(image_path)
    return jsonify({"annotation": annotation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

