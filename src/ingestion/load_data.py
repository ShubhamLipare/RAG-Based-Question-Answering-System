import PyPDF2
import sys
import os
from src.logger import logging
from src.exception import CustomException

def load_pdf(path):
    """Load text from a PDF file."""
    try:
        if not os.path.exists(path):
            logging.error(f"File not found: {path}")
            return None

        logging.info("Loading data from source...")
        with open(path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])  

        if not text.strip():
            logging.warning("Extracted text is empty. Check the PDF content.")
            return None

        logging.info("Data loaded successfully.")
        return text

    except Exception as e:
        raise CustomException(e, sys)

"""
if __name__ == "__main__":
    file_path = input("Enter path to PDF file: ").strip()
    text = load_pdf(file_path)
    
    if text:
        os.makedirs("data", exist_ok=True)
        with open("data/preprocessed_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        logging.info("Processed data saved successfully.")
"""