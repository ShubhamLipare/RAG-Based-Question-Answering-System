from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains import create_history_aware_retriever
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from src.retriever.vectorstore import VectorStore
from src.logger import logging
from src.exception import CustomException
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
import sys

class ChatBot:
    def __init__(self):
        try:
            self.vector_store = VectorStore()
            self.retriever = self.vector_store.as_retriever()
            self.store = {}  # Stores chat history for multiple sessions

            if not self.retriever:
                raise ValueError("Retriever could not be initialized")

            self.llm = ChatGroq(model="llama3-8b-8192")

            logging.info("ChatBot initialized successfully.")

        except Exception as e:
            raise CustomException(e, sys)

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Retrieve or create chat history for a session."""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]  

    def get_chat_response(self, query, session_id="default_session"):
        try:
            # System Prompt for Contextualization
            contextualize_q_system_prompt = (
                "Given a chat history and the latest user question "
                "which might reference context in the chat history, "
                "formulate a standalone question which can be understood "
                "without the chat history. Do NOT answer the question, "
                "just reformulate it if needed and otherwise return it as is."
            )

            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])

            history_aware_retriever = create_history_aware_retriever(
                self.llm, self.retriever, contextualize_q_prompt
            )

            # System Prompt for Answer Generation
            system_prompt = """
                You are a great historian with deep knowledge of Indian history.
                Given a question, try to answer it in depth by referring to the retrieved context.
                <context>
                {context}
                <context>
            """

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("user", "{input}")
            ])

            # RAG Chain
            qa_prompt = create_stuff_documents_chain(self.llm, prompt)
            rag_chain = create_retrieval_chain(history_aware_retriever, qa_prompt)

            # Add Memory
            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain,
                self.get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )

            # Dynamic session management
            configs = {"configurable": {"session_id": session_id}}

            logging.info(f"Invoking chatbot with query: {query}")
            response = conversational_rag_chain.invoke({"input": query}, config=configs)
            return response["answer"]

        except Exception as e:
            return str(CustomException(e, sys))

