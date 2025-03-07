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
