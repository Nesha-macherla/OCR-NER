import streamlit as st
import pdf2image
import pytesseract
import spacy
import tempfile
import os

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    # Create a temporary directory to store PDF pages as images
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert PDF to images
        images = pdf2image.convert_from_bytes(pdf_file.read())
        
        # Perform OCR on each image
        text = ""
        for i, image in enumerate(images):
            # Save the image temporarily
            image_path = os.path.join(temp_dir, f'page_{i}.png')
            image.save(image_path, 'PNG')
            
            # Perform OCR
            text += pytesseract.image_to_string(image_path)
    
    return text

def perform_ner(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def main():
    st.title("PDF OCR and Named Entity Recognition")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("Performing OCR and NER...")

        # Extract text from PDF using OCR
        extracted_text = extract_text_from_pdf(uploaded_file)

        # Perform NER on the extracted text
        entities = perform_ner(extracted_text)

        # Display results
        st.subheader("Extracted Text")
        st.text(extracted_text)

        st.subheader("Named Entities")
        for entity, label in entities:
            st.write(f"{entity}: {label}")

if __name__ == "__main__":
    main()
