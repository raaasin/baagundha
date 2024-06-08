import os
import pathlib
from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64
import io
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    image_data = data['image'].split(",")[1]
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    image.save('image.png')

    model = genai.GenerativeModel('gemini-1.5-flash')
    picture = {
        'mime_type': 'image/png',
        'data': pathlib.Path('image.png').read_bytes()
    }

    response = model.generate_content(
        ["Read all contents of the label, based on all contents rate it out of 5 for edible products based on health and for inedible products like groceries or makeup tell about safe usage etc,reply like this: Rating:, Reason:, expiry if mentioned:", picture],
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0
        )
    )
    response.resolve()

    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
