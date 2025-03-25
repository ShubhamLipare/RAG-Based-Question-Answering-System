import requests
import streamlit as st 
from src.logger import logging
from src.exception import CustomException
import sys

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

# Streamlit UI
st.title("Chatbot with RAG and LangChain")
st.subheader("I am expert in Data Science field!!!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id=None

try:
    logging.info("Streamlit app is live")

    session_id = st.sidebar.text_input("Enter Session ID")
    query = st.text_input("Ask a question:")

    # Clear chat history if session ID changes, it checks if session id is entered and not equal to previous session id
    if session_id and (session_id != st.session_state.session_id):
        st.session_state.chat_history = []
        st.session_state.session_id=session_id
    else:
        session_id="default"


    if st.button("Generate response"):
        if query.strip():
            try:
                logging.info(f"Sending request to FastAPI: {query}")

                payload = {"query": query}
                if session_id:
                    payload["session_id"] = session_id  # Add session_id if needed

                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "response" in data:
                        # Store and display chat history
                        st.session_state.chat_history.append(("You", query))
                        st.session_state.chat_history.append(("Bot", data["response"]))

                        logging.info("Displaying response")
                        st.write(f"**Bot:** {data['response']}")

                        # Display full chat history

                        st.subheader("Chat History")
                        for sender, msg in st.session_state.chat_history:
                            st.write(f"**{sender}:** {msg}")

                    else:
                        st.error("Unexpected API response format. Check backend logs.")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to API: {e}")
        else:
            st.warning("Please enter a query before clicking 'Generate response'.")

except Exception as e:
    logging.error(f"Streamlit app error: {str(e)}")
    raise CustomException(e, sys)
