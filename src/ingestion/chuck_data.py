from langchain.text_splitter import RecursiveCharacterTextSplitter

def chuck_text(text,chunk_size=512,overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)