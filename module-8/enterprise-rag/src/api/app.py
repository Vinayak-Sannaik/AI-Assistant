from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from src.ingestion.index_documents import index_documents
from fastapi.middleware.cors import CORSMiddleware
import json

from src.retrieval.rag_service import RAGService
# from src.rag.rag_service import RAGService
from src.api.models import (
    AskRequest,
    AskResponse,
)

from pathlib import Path

from src.api.models import (
    DocumentInfo,
    KnowledgeBaseResponse,
)

app = FastAPI()


app = FastAPI(title="RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGService()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/upload")
async def upload(
    file: UploadFile = File(...)
):
    global rag_service

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    index_documents()

    rag_service = RAGService()

    return {
        "message": "Uploaded successfully",
        "filename": file.filename,
    }


@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask(
    request: AskRequest,
):
    answer = rag.ask(
        request.question
    )

    return AskResponse(
        answer=answer
    )

@app.get(
    "/knowledge-base",
    response_model=KnowledgeBaseResponse,
)
def knowledge_base():

    documents = []

    for file in Path("data").iterdir():

        if (
            file.is_file()
            and file.name != "chunks.json"
        ):
            documents.append(
                DocumentInfo(
                    filename=file.name
                )
            )

        
    chunk_count = 0

    chunks_file = Path("data/chunks.json")

    if chunks_file.exists():

        with open(
            chunks_file,
            "r",
            encoding="utf-8",
        ) as file:
            chunk_count = len(
                json.load(file)
            )

    return KnowledgeBaseResponse(
        documents=documents,
        total_documents=len(
            documents
        ),
        total_chunks=chunk_count
    )