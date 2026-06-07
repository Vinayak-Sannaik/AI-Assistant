from src.retrieval.multi_query_generator import (
    MultiQueryGenerator
)


class MultiQueryRetriever:

    def __init__(self, retriever):
        self.retriever = retriever
        self.generator = MultiQueryGenerator()

    def search(
        self,
        question: str,
    ):
        queries = self.generator.generate(
            question
        )

        all_results = []

        for query in queries:
            print(f"\nQuery: {query}")

            results = self.retriever.search(
                query
            )

            all_results.extend(
                results
            )

        return list(
            dict.fromkeys(
                all_results
            )
        )