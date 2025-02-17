import requests
import streamlit as st 
from src.logger import logging
from src.exception import CustomException
import sys

st.title("Chatbot with RAG and Langchain")

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

try:
    logging.info("streamlit app is live")
    query=st.text_input("Ask a question.")
    if st.button("Generate response"):
        logging.info("hitting API")
        response=requests.get("http://127.0.0.1:8000/chat",params={"query":query}).json()
        logging.info("Adding chat history")
        st.session_state.chat_history.append((query,response["response"]))
        logging.info("writing response")
        for q,r in st.session_state.chat_history:
            st.write(f"**You**{q}")
            st.write(f"**Bot**{r}")
except Exception as e:
    raise CustomException(e,sys)