import sys
import streamlit as st
import spacy
import os
import shutil

# Debug information
st.write(f"Python version: {sys.version}")
st.write(f"Current working directory: {os.getcwd()}")
st.write(f"Contents of current directory: {os.listdir()}")

# Try importing modules with error handling
modules_to_import = ['pdf2image', 'pytesseract', 'PIL']
for module in modules_to_import:
    try:
        exec(f"import {module}")
        st.write(f"Successfully imported {module}")
        if module == 'pdf2image':
            st.write(f"{module} version: {eval(f'{module}.__version__')}")
    except ImportError as e:
        st.error(f"Error importing {module}: {str(e)}")

# Check for poppler
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
