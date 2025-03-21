import PyPDF2
import sys
import os
from src.logger import logging
from src.exception import CustomException

def load_pdf(folder_path):
    """Load text from a PDF file."""
    try:
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            logging.error(f"Folder not found or not a directory")
            return None

        logging.info("Loading data from source...")
        all_pdfs_text=""
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".pdf"):
                file_path=os.path.join(folder_path,filename)
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    text = "\n".join([page.extract_text() or "" for page in reader.pages])  
                    all_pdfs_text+=text+"\n"
                    logging.info(f"text is read from {filename}")

        if not all_pdfs_text.strip():
            logging.warning("Extracted text is empty. Check the PDF content.")
            return None

        logging.info("Data loaded successfully.")
        return all_pdfs_text

    except Exception as e:
        raise CustomException(e, sys)
