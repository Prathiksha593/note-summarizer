
import streamlit as st
import requests
import base64

API_KEY = "YOUR_OCR_SPACE_API_KEY"

def ocr_space_api(image_bytes):
    payload = {
        'base64Image': "data:image/png;base64," + base64.b64encode(image_bytes).decode(),
        'language': 'eng',
        'isOverlayRequired': False,
    }
    response = requests.post('https://api.ocr.space/parse/image',
                             data=payload,
                             headers={'apikey': API_KEY})
    result = response.json()
    if result['IsErroredOnProcessing']:
        st.error(result.get('ErrorMessage', ['OCR processing error'])[0])
        return ""
    return result['ParsedResults'][0]['ParsedText']

st.title("Notes Summarizer with OCR.space API")

uploaded_file = st.file_uploader("Upload an image", type=['png','jpg','jpeg'])
if uploaded_file:
    image_bytes = uploaded_file.read()
    extracted_text = ocr_space_api(image_bytes)
    st.text_area("Extracted Text", extracted_text, height=150)
