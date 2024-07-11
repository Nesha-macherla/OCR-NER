import sys
import streamlit as st
import spacy
import os
import shutil
import pkg_resources
import pdf2image
import pytesseract
from PIL import Image
import io

# Debug information
#st.write(f"Python version: {sys.version}")
#st.write(f"Current working directory: {os.getcwd()}")
#st.write(f"Contents of current directory: {os.listdir()}")

# Try importing modules with error handling
modules_to_import = ['pdf2image', 'pytesseract', 'PIL']
for module in modules_to_import:
    try:
        exec(f"import {module}")
        #st.write(f"Successfully imported {module}")
        # Get version using pkg_resources
        try:
            version = pkg_resources.get_distribution(module).version
            #st.write(f"{module} version: {version}")
        except pkg_resources.DistributionNotFound:
            #st.write(f"Could not determine version for {module}")
    except ImportError as e:
        st.error(f"Error importing {module}: {str(e)}")

# Check for poppler
poppler_path = shutil.which('pdfinfo')
#st.write(f"Poppler path: {poppler_path}")

if poppler_path is None:
    st.error("poppler-utils is not installed or not in PATH")


@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    st.write("Extracting text from PDF...")
    text = ""
    try:
        # Convert PDF to images
        images = pdf2image.convert_from_bytes(pdf_file.read())
        st.write(f"Converted PDF to {len(images)} image(s)")
        
        # Perform OCR on each image
        for i, image in enumerate(images):
            st.write(f"Processing page {i+1}")
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Perform OCR
            page_text = pytesseract.image_to_string(Image.open(io.BytesIO(img_byte_arr)))
            text += page_text + "\n\n"  # Add newlines between pages
        
        return text
    except Exception as e:
        st.error(f"Error in PDF processing: {str(e)}")
        return ""

def perform_ner(text):
    nlp = load_spacy_model()
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def main():
    st.title("PDF OCR and Named Entity Recognition")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("Performing OCR and NER...")

        extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text:
            st.subheader("Extracted Text")
            st.text(extracted_text)

            st.subheader("Named Entities")
            entities = perform_ner(extracted_text)
            for entity, label in entities:
                st.write(f"{entity}: {label}")
        else:
            st.error("Failed to extract text from the PDF.")

if __name__ == "__main__":
    main()
