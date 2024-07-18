from flask import Flask, render_template, request,jsonify
import os
import base64
import io
from PIL import Image
from googlesearch import search
import google.generativeai as genai
from dotenv import load_dotenv 
load_dotenv()


image_bytes=None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])



@app.route('/process', methods=['GET'])
def process_data():
    global image_bytes

    picture = {
        'mime_type': 'image/png',
        'data': image_bytes.getvalue()  
    }
    #update app
    response = model.generate_content(
        ["What is the commonly spoken general term for this product? only reply with single word", picture],
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0,
        )
    )

    
    response.resolve()
    product_name = response.text.strip()
    print(product_name)

    input_query = "Which is the healthiest " + product_name + " in India"
    search_results = search(input_query, num_results=5, advanced=True)

    results = ""
    for result in search_results:
        results += str(result)

    print(results)
    prompt = f"healthiest product internet search is :{results} for {product_name} in India, find only one healthy product and reply like this Alternative:, Reason:, reply in json format"
    response = model.generate_content(
        [prompt],
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0,
        )
    )
    response.resolve()
    response = response.text.replace("```", "")
    response = response.replace("null", "None")
    response = response.replace("json", "")
    response_data = eval(response)
    
    return jsonify(response_data)

@app.route('/')
def main_page():
    error=""
    return render_template('index.html',error=error)

@app.route('/scan')
def scan_page():
    return render_template('scan.html')

@app.route('/capture', methods=['POST'])
def capture_image():
    try:
        global image_bytes
        image_data = request.form['image_data']
        header, encoded = image_data.split(',', 1)
        image_data = base64.b64decode(encoded)


        image_bytes = io.BytesIO(image_data)

        safe = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]


        picture = {
        'mime_type': 'image/png',
        'data': image_bytes.getvalue()  
        }

        response = model.generate_content(
                ["Read all contents of the label, based on all contents strictly rate it out of 5 for edible products using the Australian Health Star Rating (HSR) system and mention what ingredient is bad, for inedible products like groceries or makeup rate for safety of product usage etc,reply like this: rating:, reason:, expiry:, reply in json format", picture],
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    temperature=0
                ),safety_settings=safe
            )
        response.resolve()
        response = response.text.replace("```", "")
        response = response.replace("null", "None")
        response = response.replace("json", "")
        response=eval(response)

        return render_template('results.html',response=response)
    
    except Exception as e:
        error=f"It's not you, it's not me... it's google :(, try again later, {e}"

        return render_template('index.html',error=error)
    

@app.route('/alternative')
def alternative_page():
    return render_template('alternative.html', process_function=process_data)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
