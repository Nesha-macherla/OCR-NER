
import pytesseract
import pdfplumber
import spacy
import tkinter as tk
from tkinter import filedialog

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to perform OCR using pytesseract
def perform_ocr(text):
    try:
        ocr_text = pytesseract.image_to_string(text, lang='eng')
        return ocr_text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
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
def process_pdf(pdf_path):
    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    # Step 2: Perform OCR (optional, depending on text extraction quality)
    ocr_text = pdf_text  # Placeholder, you can enhance this step with OCR library
    
    # Step 3: Perform NER on OCR text
    entities = perform_ner(ocr_text)
    
    return ocr_text, entities

# Function to open file dialog and return selected file path
def choose_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

# Example usage
if __name__ == "__main__":
    # Choose PDF file using file dialog
    print("Choose a PDF file:")
    pdf_path = choose_file()
    
    if not pdf_path:
        print("No file selected. Exiting.")
    else:
        ocr_text, entities = process_pdf(pdf_path)
        
        # Print OCR output
        print("OCR Output:")
        print(ocr_text)
        print()
        
        # Print entities found by NER
        print("Entities found by NER:")
        for entity, label in entities:
            print(f"Entity: {entity}, Label: {label}")
