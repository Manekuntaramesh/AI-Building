
import os
import openai
import google.generativeai as genai
import streamlit as st
from PIL import Image
import pyttsx3
import pytesseract
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


f = open(r"C:\Users\manne\Intership_Gen_AI\Keys\gemini_api.txt")    
OPENAI_API_KEY = f.read()
genai.configure(api_key=OPENAI_API_KEY)

# Initialize OpenAI and Google Chat models
llm = ChatGoogleGenerativeAI(google_api_key=OPENAI_API_KEY, model="gemini-1.5-flash")

# Initialize Text-to-Speech engine
# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Page Configuration
st.set_page_config(
    page_title="AI_VisionAssist",
    page_icon="🧠",
    layout="wide",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: #555;
    }
    .feature-header {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    footer {
        text-align: center;
        color: #aaa;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown('<div class="main-title">AI-VisionAssist 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Building AI Powered Solution for Assisting Visually Impaired Individuals</div>', unsafe_allow_html=True)

# Sidebar with Features and Instructions
st.sidebar.image(
    r"C:\Users\manne\Intership_Gen_AI\AI Building\360_F_559871209_pbXlOVArUal3mk6Ce60JuP13kmuIRCth.webp",
    width=200,
    caption="VisionAssist Logo",
)

st.sidebar.title("ℹ️ Detail")
st.sidebar.markdown(
    """
    ### Features:
    - 🔍 **Describe Scene**: Get AI insights about the image.
    - 📝 **Extract Text**: Use OCR to extract visible text.
    - 🔊 **Text-to-Speech**: Listen to the extracted text.
    
    ### How It Works:
    1. Upload an image.
    2. Select a feature to interact with the AI.
    """
)

st.sidebar.success("Uploaded !")

# Functions
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(prompt):
    """Generates a scene description using Google Generative AI."""
    try:
        response = llm.predict(prompt)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Main Section
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    if col1.button("🔍 Describe Scene"):
        with st.spinner("Analyzing the scene..."):
            try:
                response = generate_scene_description("Describe the scene for a visually impaired individual.")
                st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
                st.write(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")

    if col2.button("📝 Extract Text"):
        with st.spinner("Extracting text from image..."):
            try:
                text = extract_text_from_image(image)
                st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
                st.text_area("Extracted Text", text, height=150)
            except Exception as e:
                st.error(f"Error: {str(e)}")

    if col3.button("🔊 Text-to-Speech"):
        with st.spinner("Converting text to speech..."):
            try:
                text = extract_text_from_image(image)
                if text.strip():
                    text_to_speech(text)
                    st.success("Text-to-Speech conversion completed!")
                else:
                    st.warning("No text found in the image.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown(
    """
    <footer>
        Powered by <strong>Google Gemini API</strong> | Built with  using Streamlit
    </footer>
    """,
    unsafe_allow_html=True,
)
