
import streamlit as st
from PIL import Image
import pytesseract
from transformers import pipeline

st.title("Notes Summarizer & Scanner")

uploaded_file = st.file_uploader("Upload an image or a text file", type=['png','jpg','jpeg','txt'])

if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        img = Image.open(uploaded_file).convert('RGB')
        st.image(img, caption="Uploaded Image", use_column_width=True)
        text = pytesseract.image_to_string(img)
        st.text_area("Extracted Text", text, height=150)
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.getvalue().decode("utf-8")
        st.text_area("File Text", text, height=150)
    else:
        text = ""
        st.warning("Unsupported file type.")

    if text.strip():
        st.write("Generating summary...")
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(text[:1024], max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        st.subheader("Summary")
        st.write(summary)
    else:
        st.info("No text extracted to summarize.")
