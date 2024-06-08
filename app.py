import os
import pathlib
from flask import Flask, render_template, request, jsonify
from PIL import Image
import base64
import io
from googlesearch import search
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
    try:
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
            ["Read all contents of the label, based on all contents rate it out of 5 for edible products using the Australian Health Star Rating (HSR) system and for inedible products like groceries or makeup tell about safe usage etc,reply like this: rating:, reason:, expiry:, reply in json format", picture],
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0
            )
        )
        response.resolve()
        response = response.text.replace("```", "")
        response = response.replace("json", "")
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthier_alternative', methods=['POST'])
def healthier_alternative():
    try:
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
            ["What is the general term for this product? only reply with single word", picture],
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0,
            )
        )
        response.resolve()
        product_name = response.text.strip()

        input_query = "What is the healthiest " + product_name + " in India"
        search_results = search(input_query, num_results=5, advanced=True)

        results = ""
        for result in search_results:
            results += str(result)

        prompt = f"healthiest product internet search is :{results} for {product_name} in India,find only one healthy product and  reply like this Alternative:, Reason:, reply in json format"
        response = model.generate_content(
            [prompt],
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0,
            )
        )
        response.resolve()
        response = response.text.replace("```", "")
        response = response.replace("json", "")
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
