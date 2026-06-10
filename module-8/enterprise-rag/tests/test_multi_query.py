from src.retrieval.multi_query_generator import (
    MultiQueryGenerator
)

generator = MultiQueryGenerator()

queries = generator.generate(
    "What is chromaDB?"
)

for query in queries:
    print(query)