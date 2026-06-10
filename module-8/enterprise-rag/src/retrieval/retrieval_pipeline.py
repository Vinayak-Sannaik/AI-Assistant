from src.retrieval.reranker import Reranker
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.multi_query_generator import (
    MultiQueryGenerator,
)

import json


MIN_BEST_SCORE = -8


class RetrievalPipeline:

    def __init__(self):

        vector_store = VectorStore()

        bm25 = BM25Retriever()
        bm25.load_from_disk()

        self.retriever = HybridRetriever(
            vector_store,
            bm25,
        )

        self.multi_query = (
            MultiQueryGenerator()
        )

        self.reranker = Reranker()

    def retrieve(
        self,
        query: str,
        top_k: int = 8,
        source: str | None = None,
    ):

        original_query = query

        if source:

            queries = [
                original_query
            ]

            generated_queries = []

        else:

            generated_queries = (
                self.multi_query.generate(
                    original_query
                )
            )

            queries = list(
                dict.fromkeys(
                    [
                        original_query,
                        *generated_queries,
                    ]
                )
            )

        print("\nGenerated Queries:")

        for query_variant in queries:
            print("->", query_variant)

        all_results = []

        for query_variant in queries:

            results = self.retriever.search(
                query_variant,
                top_k=top_k,
                source=source,
            )

            all_results.extend(
                results
            )

        if not all_results:
            return {
                "retrieved_documents": [],
                "generated_queries": generated_queries,
            }

        unique_results = {}

        for doc in all_results:

            unique_results[
                doc.chunk_id
            ] = doc

        results = list(
            unique_results.values()
        )

        print(
            f"\nRetrieved: {len(all_results)}"
        )

        print(
            f"Unique: {len(results)}"
        )

        # Larger candidate pool before reranking
        results = results[:50]

        reranked = self.reranker.rerank(
            original_query,
            results,
            top_k=top_k,
        )

        print("\nReranked:")

        for doc, score in reranked:
            print(score)
            print(doc)

        if not reranked:
            return {
                "retrieved_documents": [],
                "generated_queries": generated_queries,
            }

        best_score = reranked[0][1]

        print(
            f"\nBest Score: {best_score}"
        )

        best_score = reranked[0][1]

        threshold = best_score - 2

        filtered_reranked = [
            (doc, score)
            for doc, score in reranked
            if score >= threshold
        ]

        if filtered_reranked:
            reranked = filtered_reranked

        print(
            f"Threshold: {threshold}"
        )

        print(
            f"Final: {len(reranked)}"
        )

        return {
            "retrieved_documents": [
                {
                    "content": doc.content,
                    "source": doc.source,
                    "chunk_id": doc.chunk_id,
                    "score": float(score),
                }
                for doc, score in reranked
            ],
            "generated_queries": generated_queries,
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