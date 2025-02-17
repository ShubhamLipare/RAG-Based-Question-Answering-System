from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
from src.logger import logging
from src.exception import CustomException

def chuck_text(text,chunk_size=512,overlap=100):

    try:
        logging.info("Text splitting has begun")
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)

        logging.info("Returning splitted text")
        return splitter.split_text(text)
    except Exception as e:
        raise CustomException(e,sys)
