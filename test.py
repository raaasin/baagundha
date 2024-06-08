import pathlib
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

img = {
    'mime_type': 'image/png',
    'data': pathlib.Path('image.png').read_bytes()
}

response=model.generate_content(["Read all contents of the label, based on all contents rate it out of 5 for edible products healthy diet, for unedible safe usage etc, only reply with rating and nothing else", img],generation_config=genai.types.GenerationConfig(
        # Only one candidate for now.
        candidate_count=1,
        stop_sequences=['x'],
        max_output_tokens=20,
        temperature=0))
response.resolve()
print(response.text)
