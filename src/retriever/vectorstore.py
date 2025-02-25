import os
import sys
import numpy as np
from langchain_community.vectorstores import FAISS  
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.logger import logging
from src.exception import CustomException

class VectorStore:
    def __init__(self, index_path="data/vectorestore.index"):
        try:
            self.index_path = index_path
            self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            logging.info("VectorStore initialized successfully.")

            os.makedirs(index_path, exist_ok=True)
            index_file = os.path.join(index_path, "index.faiss")

            if os.path.exists(index_file):
                logging.info(f"Loading existing FAISS index from {index_file}...")
                self.vector_store = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
            else:
                logging.info("No saved FAISS index found. Creating a new one...")
                self.vector_store = FAISS.from_texts(["dummy text"], self.embeddings)  # Initialize with dummy as it doesnt accept empty list
                self.vector_store.save_local(index_path)

        except Exception as e:
            raise CustomException(e, sys)

    def add_text(self, texts):
        """Add text chunks to FAISS index with embeddings."""
        try:
            if isinstance(texts, str):
                texts = [texts]
            elif not isinstance(texts, list) or not all(isinstance(t, str) for t in texts):
                raise ValueError("Texts should be a string or a list of strings.")

            if not texts:
                logging.warning("Received empty text list. Skipping FAISS update.")
                return

            logging.info(f"Generating embeddings for {len(texts)} texts...")
            embeddings = self.embeddings.embed_documents(texts)

            if self.vector_store.index.ntotal == 0:
                self.vector_store = FAISS.from_embeddings(embeddings, texts)
            else:
                self.vector_store.add_texts(texts)

            self.vector_store.save_local(self.index_path)
            logging.info(f"Successfully added {len(texts)} texts to FAISS index.")

        except Exception as e:
            raise CustomException(e, sys)

    def as_retriever(self):
        """Returns a retriever from the FAISS index."""
        return self.vector_store.as_retriever(search_kwargs={"k": 10})

    def search(self, query, k=5):
        """Search FAISS for similar results."""
        try:
            logging.info(f"Searching FAISS for: {query}")
            retriever = self.as_retriever()
            docs = retriever.invoke(query)[:k]

            if not docs:
                logging.warning("No relevant documents found.")
            
            return docs

        except Exception as e:
            raise CustomException(e, sys)
