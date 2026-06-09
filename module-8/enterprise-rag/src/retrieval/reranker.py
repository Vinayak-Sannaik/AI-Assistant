from sentence_transformers import CrossEncoder
from src.retrieval.retrieval_document import RetrievalDocument


class Reranker:

    def __init__(self):
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        documents: list[RetrievalDocument],
        top_k: int = 5,
    ):

        pairs = [
            [query, doc.content]
            for doc in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:top_k]