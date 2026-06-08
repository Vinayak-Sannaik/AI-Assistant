from src.retrieval.reranker import Reranker
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever


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
        top_k: int = 3,
    ):

        results = self.retriever.search(
            query,
            top_k=top_k,
        )

        reranked = self.reranker.rerank(
            query,
            results,
            top_k=top_k,
        )

        return [
            doc
            for doc, _score in reranked
        ]