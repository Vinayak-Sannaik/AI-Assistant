from rank_bm25 import BM25Okapi
from src.configg.settings import TOP_K_RERANK
import json
from langchain_core.documents import Document


class BM25Retriever:

    def __init__(self):
        self.bm25 = None
        self.documents = []

    def index(self, documents):
        self.documents = documents

        tokenized_docs = [
            doc.page_content.lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(tokenized_docs)

    def search(
        self,
        query: str,
        top_k: int = TOP_K_RERANK,
    ):
        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked[:top_k]

    def load_from_disk(
        self,
        path: str = "data/chunks.json",
    ):
        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        self.documents = [
            Document(
                page_content=item["content"],
                metadata=item["metadata"],
            )
            for item in data
        ]

        tokenized_docs = [
            doc.page_content.lower().split()
            for doc in self.documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_docs
        )