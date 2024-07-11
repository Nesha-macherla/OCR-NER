import sys
import streamlit as st
import pytesseract
from PIL import Image
import spacy
import tempfile
import os
from pdf2image import convert_from_bytes
import shutil


# Debug information
st.write(f"Python version: {sys.version}")
st.write(f"spaCy version: {spacy.__version__}")
st.write(f"pdf2image version: {pdf2image.__version__}")
st.write(f"Tesseract version: {pytesseract.get_tesseract_version()}")
st.write("Imported modules:")
st.write(f"pdf2image: {'pdf2image' in sys.modules}")
st.write(f"pytesseract: {'pytesseract' in sys.modules}")
st.write(f"spacy: {'spacy' in sys.modules}")

poppler_path = shutil.which('pdfinfo')
st.write(f"Poppler path: {poppler_path}")

if poppler_path is None:
    st.error("poppler-utils is not installed or not in PATH")
# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            images = pdf2image.convert_from_bytes(pdf_file.read())
            
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f'page_{i}.png')
                image.save(image_path, 'PNG')
                
                text += pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        st.error(f"Error in PDF processing: {str(e)}")
        return ""

# Load the spaCy model
@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError as e:
        st.error(f"Error loading spaCy model: {str(e)}")
        return None

nlp = load_model()

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            images = convert_from_bytes(pdf_file.read())
            
            for i, image in enumerate(images):
                image_path = os.path.join(temp_dir, f'page_{i}.png')
                image.save(image_path, 'PNG')
                
                text += pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        st.error(f"Error in PDF processing: {str(e)}")
        return ""

def perform_ner(text):
    if nlp is None:
        return []
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def main():
    st.title("PDF OCR and Named Entity Recognition")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("Performing OCR and NER...")

        extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text:
            st.subheader("Extracted Text")
            st.text(extracted_text)

            entities = perform_ner(extracted_text)

            st.subheader("Named Entities")
            for entity, label in entities:
                st.write(f"{entity}: {label}")
        else:
            st.error("Failed to extract text from the PDF.")

if __name__ == "__main__":
    main()
