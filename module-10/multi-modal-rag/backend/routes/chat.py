from fastapi import APIRouter

from schemas.chat import ChatRequest
from services.retriever import retrieve
from services.llm import generate_answer

router = APIRouter()


@router.post("/ask")
def ask(request: ChatRequest):

    context, docs = retrieve(
        request.question
    )

    answer = generate_answer(
        request.question,
        context
    )

    return {
        "answer": answer,
        "chunks": [
            doc.page_content
            for doc in docs
        ]
    }