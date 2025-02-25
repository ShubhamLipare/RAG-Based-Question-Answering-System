# run by command : uvicorn src.api.api:app --host 0.0.0.0 --port 8000 --reload
#mlflow manual start: mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 5000

from fastapi import FastAPI, HTTPException
import mlflow
from pydantic import BaseModel
from src.generator.chat_pipeline import ChatBot
from src.exception import CustomException
from src.logger import logging
import sys

# Initialize FastAPI
app = FastAPI()

# Set up MLflow tracking
mlflow.set_tracking_uri("http://localhost:5000")  
mlflow.set_experiment("rag_chat_experiment")

# Initialize chatbot
chatbot = ChatBot()

# Request Model
class ChatRequest(BaseModel):
    query: str
    session_id:str


@app.post("/chat")
def chat(request: ChatRequest):
    """Handles chat requests and logs to MLflow."""
    try:
        query = request.query
        session_id = request.session_id
        logging.info(f"Received query: {query}")

        # Get chatbot response
        response = chatbot.get_chat_response(query,session_id)
        chat_history=chatbot.get_session_history(session_id).messages
        
        # Log query and response length to MLflow
        logging.info("Logging to MLflow...")
        with mlflow.start_run():
            mlflow.log_param("session_id", session_id)
            mlflow.log_param("query", query)
            mlflow.log_metric("response_length", len(response))

        # Return response
        return {"response": response, "chat_history":chat_history }

    except Exception as e:
        logging.error(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Chatbot API is running"}
