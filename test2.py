import sys
import streamlit as st
import spacy
import os
import shutil
import pkg_resources

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
        # Get version using pkg_resources
        try:
            version = pkg_resources.get_distribution(module).version
            st.write(f"{module} version: {version}")
        except pkg_resources.DistributionNotFound:
            st.write(f"Could not determine version for {module}")
    except ImportError as e:
        st.error(f"Error importing {module}: {str(e)}")

# Check for poppler
poppler_path = shutil.which('pdfinfo')
st.write(f"Poppler path: {poppler_path}")

if poppler_path is None:
    st.error("poppler-utils is not installed or not in PATH")

# List all installed packages and their versions
st.write("Installed packages:")
installed_packages = pkg_resources.working_set
installed_packages_list = sorted([f"{i.key} == {i.version}" for i in installed_packages])
for package in installed_packages_list:
    st.write(package)

# Test PDF processing
import pdf2image
import io
from PIL import Image

def test_pdf_processing():
    st.write("Testing PDF processing...")
    # Create a simple PDF in memory
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 100, "Hello world!")
    c.showPage()
    c.save()

    buffer.seek(0)
    
    try:
        images = pdf2image.convert_from_bytes(buffer.getvalue())
        st.write(f"Successfully converted PDF to {len(images)} image(s)")
        st.image(images[0], caption="Converted PDF page", use_column_width=True)
    except Exception as e:
        st.error(f"Error in PDF processing: {str(e)}")

test_pdf_processing()

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
