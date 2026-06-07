from src.retrieval.multi_query_generator import (
    MultiQueryGenerator
)

generator = MultiQueryGenerator()

queries = generator.generate(
    "How can I store semantic search data?"
)

for query in queries:
    print(query)