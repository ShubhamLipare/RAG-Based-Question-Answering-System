from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
import os
from src.logger import logging
from src.exception import CustomException

def chunk_text(text, chunk_size=1024, overlap=200):
    """Splits text into smaller chunks for vectorization."""
    try:
        if not text or not text.strip():
            logging.error("Received empty text for splitting.")
            return []

        logging.info("Splitting text into chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        chunks = splitter.split_text(text)

        if not chunks:
            logging.warning("Text splitting resulted in no chunks. Check input size.")
        
        return chunks

    except Exception as e:
        raise CustomException(e, sys)
    
"""

if __name__ == "__main__":
    if not os.path.exists("data/preprocessed_text.txt"):
        logging.error("Preprocessed text file not found. Run load.py first.")
        sys.exit(1)

    with open("data/preprocessed_text.txt", "r", encoding="utf-8") as file:
        text = file.read()

    splitted_text = chunk_text(text)

    if splitted_text:
        os.makedirs("data", exist_ok=True)
        with open("data/splitted.txt", "w", encoding="utf-8") as f:
            for chunk in splitted_text:
                f.write(chunk + "\n")

        logging.info(f"Successfully saved {len(splitted_text)} text chunks.")
"""