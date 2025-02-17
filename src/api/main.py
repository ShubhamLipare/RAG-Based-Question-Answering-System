from fastapi import FastAPI
from generator.chat_pipeline import chatbot
import mlflow
from src.exception import CustomException
from src.logger import logging
import sys

app=FastAPI()
mlflow.set_tracking_url("http://localhost:5000")
mlflow.set_experiment("rag_chat_experiment")

@app.get("/chat")
def chat(query:str):
    try:
        logging.info("generating response")
        response=chatbot.get_chat_response(query)
        logging.info("starting mlflow logging")
        with mlflow.start_run():
            mlflow.log_param("query",query)
            mlflow.log_metric("response_length",len(response))
        return {"response":response,"chat_history":chatbot.memory.messages}
    
    except Exception as e:
        raise CustomException(e,sys)