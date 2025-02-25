# RAG-Based Question Answering System

## 📌 Overview
This project implements a **Retrieval-Augmented Generation (RAG)** based chatbot using **LangChain**, **FastAPI**, **Streamlit**, **FAISS/ChromaDB**, and **MLflow**. It combines a **retriever** (vector database) with a **generator** (LLM-based response generation) to answer user queries effectively.

## 🏗️ Project Structure
```
RAG-Based-Chatbot/
│── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api.py  # FastAPI backend
│   ├── generator/
│   ├── ingestion/
│   ├── retriever/
│   ├── logger.py
│   ├── exception.py
│── ui/
│   ├── __init__.py
│   ├── app.py  # Streamlit frontend
│── requirements.txt
│── README.md
```

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/rag-chatbot.git
cd rag-chatbot
```

### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up MLflow Tracking Server
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000
```

### 5️⃣ Start FastAPI Server
```bash
uvicorn src.api.api:app --host 0.0.0.0 --port 8000 --reload
```

### 6️⃣ Start Streamlit UI
```bash
streamlit run src/ui/app.py
```

## 🛠️ How It Works
1. **Data Ingestion**: Loads and preprocesses the documents.
2. **Vector Store**: Converts text into embeddings and stores them in FAISS/ChromaDB.
3. **Query Processing**: Retrieves relevant chunks using vector similarity search.
4. **Response Generation**: Uses a language model (LLM) to generate contextual responses.

## 📡 API Endpoints
| Method | Endpoint  | Description |
|--------|----------|-------------|
| `GET`  | `/chat`  | Generates a chatbot response based on a query |

### Example API Call
```bash
curl "http://127.0.0.1:8000/chat?query=Tell me about RAG"
```

## 🖥️ Running the Application
- Open **[http://127.0.0.1:8501](http://127.0.0.1:8501)** in your browser for the Streamlit UI.
- Enter your query and interact with the chatbot.

## 🔥 Troubleshooting
### ❌ FastAPI not running
- Run `uvicorn src.api.api:app --host 0.0.0.0 --port 8000 --reload`
- Check if port **8000** is occupied (`netstat -ano | findstr :8000`)

### ❌ Streamlit UI not loading
- Check logs for errors (`streamlit run src/ui/app.py`)
- Ensure FastAPI is running first

### ❌ MLflow errors
- Ensure MLflow is running (`mlflow server --host 0.0.0.0 --port 5000`)
- Set tracking URI correctly in `api.py`

## ✨ Future Enhancements
- 🔹 Deploy API using **Docker & Kubernetes**
- 🔹 Add **authentication & user history tracking**
- 🔹 Fine-tune **LLM for domain-specific responses**

---
### 🎯 Contributors
- **Your Name** - Developer
- **Your Team** - Collaborators

📩 **Have issues?** Open an issue or reach out!

---
🔗 **GitHub Repository:** [Your Repo](https://github.com/your-repo/rag-chatbot)

