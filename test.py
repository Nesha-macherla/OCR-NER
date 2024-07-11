import streamlit as st
import pytesseract
import pdfplumber
import spacy
from spacy import en_core_web_sm

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to perform OCR using pytesseract
def perform_ocr(image_path):
    try:
        ocr_text = pytesseract.image_to_string(image_path, lang='eng')
        return ocr_text.strip()
    except Exception as e:
        st.error(f"OCR Error: {e}")
        return ""

# Function to perform NER using spaCy
def perform_ner(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

# Main function to process PDF, perform OCR, and NER
def process_pdf(pdf_file):
    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_file)
    
    # Step 2: Perform OCR (optional, depending on text extraction quality)
    ocr_text = pdf_text  # Placeholder, you can enhance this step with OCR library
    
    # Step 3: Perform NER on OCR text
    entities = perform_ner(ocr_text)
    
    return ocr_text, entities

# Streamlit app
def main():
    st.title("PDF OCR EXTRACTION and NER")
    
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Display file details
        st.sidebar.header('File Details')
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
        st.sidebar.write(file_details)
        
        # Process PDF and display results
        ocr_text, entities = process_pdf(uploaded_file)
        
        # Display OCR output
        st.subheader("OCR Output:")
        st.write(ocr_text)
        
        # Display NER entities
        st.subheader("Entities found by NER:")
        for entity, label in entities:
            st.write(f"Entity: {entity}, Label: {label}")

if __name__ == "__main__":
    main()
