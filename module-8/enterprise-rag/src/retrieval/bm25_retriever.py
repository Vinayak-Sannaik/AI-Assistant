from rank_bm25 import BM25Okapi
from src.configg.settings import TOP_K_RERANK
import json
from langchain_core.documents import Document
from src.retrieval.retrieval_document import RetrievalDocument

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
        source: str | None = None,
    ):
        tokenized_query = query.lower().split()

        if source is None:

            documents = self.documents
            bm25 = self.bm25

        else:

            documents = [
                doc
                for doc in self.documents
                if doc.metadata.get("source") == source
            ]

            if not documents:
                return []

            tokenized_docs = [
                doc.page_content.lower().split()
                for doc in documents
            ]

            bm25 = BM25Okapi(
                tokenized_docs
            )

        scores = bm25.get_scores(
            tokenized_query
        )

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        results = []

        for doc, score in ranked[:top_k]:

            retrieval_doc = RetrievalDocument(
                content=doc.page_content,
                source=doc.metadata.get(
                    "source",
                    "Unknown",
                ),
                chunk_id=doc.metadata.get(
                    "chunk_id",
                ),
            )

            results.append(
                (
                    retrieval_doc,
                    score,
                )
            )

        return results

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