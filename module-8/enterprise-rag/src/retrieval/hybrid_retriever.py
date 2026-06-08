from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.rrf import reciprocal_rank_fusion
from src.retrieval.base_retriever import BaseRetriever

class HybridRetriever(BaseRetriever):

    def __init__(
        self,
        vector_store: VectorStore,
        bm25_retriever: BM25Retriever,
    ):
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever

    def search(
        self,
        query: str,
        top_k: int = 5,
        source: str | None = None,
    ):
        chroma_results = self.vector_store.search(
            query,
            top_k=top_k,
            source=source
        )

        bm25_results = self.bm25_retriever.search(
            query,
            top_k=top_k,
            source=source
        )

        vector_ranked = chroma_results["documents"][0]
        bm25_ranked = [
            doc.page_content
            for doc, _score in bm25_results
        ]

        fused_results = reciprocal_rank_fusion(
            [
                bm25_ranked,
                vector_ranked,
            ]
        )

        # print("\nBM25 Ranking")
        # for doc in bm25_ranked:
        #     print(doc)

        # print("\nVector Ranking")
        # for doc in vector_ranked:
        #     print(doc)

        # print("\nFused Ranking")
        # for doc, score in fused_results:
        #     print(score, doc)

        return [
            document
            for document, _score
            in fused_results
        ]


        # merged_documents = []

        # for doc in chroma_results["documents"][0]:
        #     merged_documents.append(doc)

        # for doc, _score in bm25_results:
        #     merged_documents.append(
        #         doc.page_content
        #     )

        # return list(
        #     dict.fromkeys(
        #         merged_documents
        #     )
        # )