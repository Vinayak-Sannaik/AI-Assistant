from fastapi import FastAPI, UploadFile, File
from pathlib import Path
from src.ingestion.index_documents import index_documents
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path
from fastapi import HTTPException

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
    global rag

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    index_documents()

    rag = RAGService()

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
    result = rag.ask(
        request.question
    )

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
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

@app.delete(
    "/knowledge-base/{filename}"
)
def delete_document(
    filename: str,
):
    file_path = Path(
        "data"
    ) / filename

    if filename == "chunks.json":
        raise HTTPException(
            status_code=400,
            detail="Protected file",
        )

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    file_path.unlink()

    indexed_chunks = (
        index_documents()
    )

    global rag

    rag = RAGService()

    return {
        "message": f"{filename} deleted",
        "remaining_documents": len(
            [
                f
                for f in Path("data").iterdir()
                if f.is_file()
                and f.name != "chunks.json"
            ]
        ),
        "indexed_chunks": indexed_chunks,
    }