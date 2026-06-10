from src.retrieval.reranker import Reranker
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.multi_query_generator import MultiQueryGenerator
from src.retrieval.multi_hop_planner import MultiHopPlanner
from src.retrieval.query_classifier import QueryClassifier

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
        self.multi_hop = MultiHopPlanner()
        self.query_classifier = QueryClassifier()
        

    def retrieve(
        self,
        query: str,
        top_k: int = 8,
        source: str | None = None,
    ):

        original_query = query

        is_multi_hop = (
            self.query_classifier.is_multi_hop(
                query
            )
        )

        # ---------------------------
        # Multi-Hop Planning
        # ---------------------------

        if source:

            hop_queries = [
                original_query
            ]

        else:

            hop_queries = (
                self.multi_hop.generate_steps(
                    original_query
                )
            )

            if not hop_queries:
                hop_queries = [
                    original_query
                ]

        print("\nMulti-Hop Queries:")

        for hop in hop_queries:
            print("->", hop)

        all_results = []

        generated_queries = []

        # ---------------------------
        # Multi Query Retrieval
        # ---------------------------

        for hop_query in hop_queries:

            if source:

                queries = [
                    hop_query
                ]

            else:

                mq_queries = (
                    self.multi_query.generate(
                        hop_query
                    )
                )

                queries = list(
                    dict.fromkeys(
                        [
                            hop_query,
                            *mq_queries,
                        ]
                    )
                )

                generated_queries.extend(
                    mq_queries
                )

            print(
                f"\nQueries for hop: {hop_query}"
            )

            for q in queries:
                print("   ->", q)

            for query_variant in queries:

                results = self.retriever.search(
                    query_variant,
                    top_k=top_k,
                    source=source,
                )

                all_results.extend(
                    results
                )

        # ---------------------------
        # No Results
        # ---------------------------

        if not all_results:
            return {
                "retrieved_documents": [],
                "generated_queries": generated_queries,
                "multi_hop_queries": hop_queries,
            }

        # ---------------------------
        # Deduplicate
        # ---------------------------

        unique_results = {}

        for doc in all_results:

            unique_results[
                (
                    doc.source,
                    doc.chunk_id,
                )
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

        # ---------------------------
        # Candidate Pool
        # ---------------------------

        results = results[:50]

        # ---------------------------
        # Cross Encoder Reranking
        # ---------------------------

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
                "multi_hop_queries": hop_queries,
            }

        # ---------------------------
        # Adaptive Filtering
        # ---------------------------

        best_score = reranked[0][1]

        print(
            f"\nBest Score: {best_score}"
        )

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

        # ---------------------------
        # Response
        # ---------------------------

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
            "generated_queries": list(
                dict.fromkeys(
                    generated_queries
                )
            ),
            "multi_hop_queries": hop_queries,
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