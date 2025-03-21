from src.ingestion.load_data import load_pdf
from src.ingestion.chuck_data import chunk_text
from src.retriever.vectorstore import VectorStore
from src.generator.chat_pipeline import ChatBot
from src.logger import logging
from src.util import source_file_path


def main():
    logging.info("Starting main pipeline")

    text=load_pdf(source_file_path)
    with open("data/extracted_data.txt","w",encoding="utf-8") as file:
        file.write(text)
    if text is None:
        logging.error("failed to load PDF, exiting")
        return None
      
    logging.info("splitting into chucnks")
    chunks=chunk_text(text)
    if not chunks:
        logging.error("Text chunking failed. Exiting.")
        return
    
    logging.info("Storing text in vector database...")
    vectore_store=VectorStore()
    vectore_store.add_text(chunks)

    logging.info("Initializing chatbot...")
    chatbot = ChatBot()

    query = "how many GENAI interview question does provided pdf has"
    logging.info(f"Running query: {query}")
    response = chatbot.get_chat_response(query)
    print("\nChatbot Response:\n", response)
    

if __name__=="__main__":
    main()