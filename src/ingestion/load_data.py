import PyPDF2
import sys
from src.logger import logging
from src.exception import CustomException

def load_pdf(path):

    try:
        logging.info("Loading data from source")
        with open(path,"rb") as file_path:
            reader=PyPDF2.PdfFileReader(file_path)
            text="".join([page.extract_text() for page in reader])

        logging.info("Data loaded sucessfully, returning text")
        return text
    
    except Exception as e:
        raise CustomException(e,sys)

