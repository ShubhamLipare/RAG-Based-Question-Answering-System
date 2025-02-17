from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from src.retriever.vectorstore import VectorStore
from src.logger import logging
from src.exception import CustomException
import sys

class ChatBot:
    def __init__(self):

        try:
            self.retriever=VectorStore()
            self.memory=ChatMessageHistory()
            self.chain=create_history_aware_retriever(
                create_retrieval_chain(create_stuff_documents_chain(ChatGroq(model="Llama3-8b-8192"))),
                self.memory
            )
            logging.info("Vectorestore, memory and chain have been initialized")
        except Exception as e:
            raise CustomException(e,sys)

    def get_chat_response(self,query):

        try:
            logging.info("Invoking chain")
            self.chain.invoke({"input":query})

        except Exception as e:
            CustomException(e,sys)
            

chatbot=ChatBot()
