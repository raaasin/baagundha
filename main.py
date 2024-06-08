import streamlit as st
from PIL import Image
import os
import pathlib
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

st.title("Webcam Capture")

# Add some CSS to make the camera input more responsive
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stCameraInput div {
        width: 100% !important;
        max-width: 500px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

img_file_buffer = st.camera_input("Capture an image")

if img_file_buffer is not None:
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Convert the image buffer to an image
    image = Image.open(img_file_buffer)
    image.save('image.png')
    picture = {
        'mime_type': 'image/png',
        'data': pathlib.Path('image.png').read_bytes()
    }

    response = model.generate_content(
        ["Read all contents of the label, based on all contents rate it out of 5 for edible products healthy diet, for unedible safe usage etc,reply like this: Rating out of 5, Reason, expiry if mentioned", picture],
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0
        )
    )
    response.resolve()
    st.text_area("Response", response.text)