from src.retrieval.reranker import Reranker
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
import json

MIN_BEST_SCORE = -80


class RetrievalPipeline:

    def __init__(self):

        vector_store = VectorStore()

        bm25 = BM25Retriever()
        bm25.load_from_disk()

        self.retriever = HybridRetriever(
            vector_store,
            bm25,
        )

        self.reranker = Reranker()

    def retrieve(
        self,
        query: str,
        top_k: int = 8,
        source: str | None = None,
    ):

        results = self.retriever.search(
            query,
            top_k=top_k,
            source=source,
        )

        if not results:
            return {
                "retrieved_documents": []
            }

        reranked = self.reranker.rerank(
            query,
            results,
            top_k=top_k,
        )

        print("\nReranked:")

        for doc, score in reranked:
            print(score)
            print(doc)

        best_score = reranked[0][1]

        print(
            f"\nBest Score: {best_score}"
        )

        if best_score < MIN_BEST_SCORE:

            print(
                "\nRetrieval rejected due to low relevance"
            )

            return {
                "retrieved_documents": []
            }

        return {
            "retrieved_documents": [
                {
                    "content": doc.content,
                    "source": doc.source,
                    "chunk_id": doc.chunk_id,
                    "score": float(score),
                }
                for doc, score in reranked
            ]
        }

    def get_document_chunks(
        self,
        source: str,
    ):
        with open(
            "data/chunks.json",
            "r",
            encoding="utf-8",
        ) as file:

            chunks = json.load(file)

        return [
            chunk["content"]
            for chunk in chunks
            if chunk["metadata"].get(
                "source"
            ) == source
        ]