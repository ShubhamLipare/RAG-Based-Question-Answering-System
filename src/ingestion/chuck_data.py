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
    