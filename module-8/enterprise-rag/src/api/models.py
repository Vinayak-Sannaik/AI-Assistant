from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


class DocumentInfo(BaseModel):
    filename: str


class KnowledgeBaseResponse(BaseModel):
    documents: list[DocumentInfo]
    total_documents: int
    total_chunks: int

