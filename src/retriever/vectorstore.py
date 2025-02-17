import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
import sys
from src.logger import logging
from src.exception import CustomException


class VectorStore:
    def __init__(self):
        try:
            self.index=faiss.IndexFlatL2(384)
            self.embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            logging.info("VectorStore initialized successfully.")

        except Exception as e:
            raise CustomException(e,sys)

    def add_text(self,texts):
        try:
            logging.info("Generating embeddings for input texts...")
            vectors=self.embeddings.embed_documents(texts) # Returns list of embeddings
            vectors=np.array(vectors,dtype=np.float32) # Convert to NumPy array
            self.index.add(vectors)
            logging.info(f"Successfully added {len(texts)} texts to the vector index.")

        except Exception as e:
            raise CustomException(e,sys)

    def search(self,query,k=5):

        try :
            logging.info(f"Searching for query: {query}")
            query_vec=np.array([self.embeddings.embed_query(query)],dtype=np.float32)
            _,I =self.index.search(query_vec,k)
            logging.info(f"Search completed. Retrieved top {k} results.")
            return I

        except Exception as e:
            raise CustomException(e,sys)