import streamlit as st
from PIL import Image
import os
import pathlib
import google.generativeai as genai
from dotenv import load_dotenv
from googlesearch import search
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

st.title("Webcam Capture")

def alternative_product(input: str):
    """returns a string of internet search of best or healthy alternative indian product for the given input product"""
    input_query = "What is the healthiest " + input + " in India"
    search_results = search(input_query, num_results=5, advanced=True)
    results=""
    for i in search_results:
        results+=str(i)
    return results


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
        ["Read all contents of the label, based on all contents rate it out of 5 for edible products based on health and for inedible products like groceries or makeup tell about safe usage etc,reply like this: Rating:, Reason:, expiry if mentioned:, reply in json format", picture],
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            temperature=0
        )
    )
    response.resolve()
    #remove ``` from the response`
    response = response.text.replace("```", "")
    response = response.replace("json", "")
    st.text(response)

    if st.button("Suggest alternative product"):
        with st.spinner("Identifying Product Name"):
            response = model.generate_content(
                ["what is this? just tell the name nothing else", picture],
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    temperature=0,
                )
            )
            response.resolve()
            product_name = response.text.strip()

        with st.spinner("Searching the internet"):
            result = alternative_product(product_name)

        with st.spinner("Almost done!"):
            prompt = f"the best alternative product is {result} for {product_name} in India, reply like this Alternative:, Reason:, reply in json format"
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
            st.text(response)
