import streamlit as st
import pytesseract
import spacy
from PIL import Image

# Download spaCy model (en_core_web_sm) if not already installed
nlp = spacy.load('en_core_web_sm')  # Download model on first run

def extract_text_from_pdf(pdf_path):
  """
  Extracts text from a PDF file using PyTesseract.

  Args:
      pdf_path: Path to the PDF file.

  Returns:
      str: Extracted text from the PDF.
  """
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update Tesseract path if needed
  pdf_image = Image.open(pdf_path)
  text = pytesseract.image_to_string(pdf_image)
  return text

def perform_ner(text):
  """
  Performs Named Entity Recognition (NER) on the given text using spaCy.

  Args:
      text: The text to perform NER on.

  Returns:
      list: List of dictionaries containing entity text, label, and starting/ending indexes.
  """
  doc = nlp(text)
  entities = []
  for ent in doc.ents:
    entities.append({
      "text": ent.text,
      "label": ent.label_,
      "start": ent.start_char,
      "end": ent.end_char,
    })
  return entities

def main():
  """
  Streamlit app to upload PDF, perform OCR and NER, and display results.
  """
  st.title("PDF OCR and Named Entity Recognition App")
  uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

  if uploaded_file is not None:
    # Read the uploaded PDF file
    bytes_data = uploaded_file.read()
    pdf_path = f"temp_pdf.{uploaded_file.name.split('.')[-1]}"
    with open(pdf_path, "wb") as f:
      f.write(bytes_data)

    # Extract text using OCR
    extracted_text = extract_text_from_pdf(pdf_path)

    # Perform NER on the extracted text
    entities = perform_ner(extracted_text)

    # Display extracted text and NER results
    st.subheader("Extracted Text")
    st.write(extracted_text)
    st.subheader("Named Entities")
    st.dataframe(entities)

if __name__ == "__main__":
  main()

