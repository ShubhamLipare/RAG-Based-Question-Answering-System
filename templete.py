import os
from pathlib import Path

folder_list =[
    f"data/",
    f"embeddings",
    f"src/__init__.py",
    f"src/ingestion/__init__.py",
    f"src/ingestion/load_data.py",
    f"src/ingestion/chunk_data.py",
    f"src/retriever/__init__.py",
    f"src/retriever/vectorstore.py",
    f"src/generator/__init__.py",
    f"src/generator/chat_pipeline.py",
    f"src/api/__init__.py",
    f"src/api/main.py",
    f"src/logger.py",
    f"src/exception.py",
    f"mlflow/__init__.py",
    f"mlflow/train.py",
    f"mlflow/config.yaml",
    f"tests/",
    f"ui/__init__.py",
    f"ui/app.py",
    f".github/workflows/ci_cd.yml",
    f"requirements.txt"
]


for path in folder_list:
    path=Path(path)

    file_dir,filename=os.path.split(path)

    if file_dir!="":
        os.makedirs(file_dir,exist_ok=True)

    if not (os.path.exists(path)) or os.path.getsize(path)==0:
        path.touch()
    else:
        print(f"{path} already exists")

