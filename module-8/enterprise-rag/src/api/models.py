from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    source: str | None = None

class DocumentInfo(BaseModel):
    filename: str


class KnowledgeBaseResponse(BaseModel):
    documents: list[DocumentInfo]
    total_documents: int
    total_chunks: int


class Citation(BaseModel):
    source: str
    chunk_id: int | None
    score: float


class DebugInfo(BaseModel):
    retrieval_query: str | None = None
    chunks_used: int
    mode: str | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    citations: list[Citation]
    debug: DebugInfo

