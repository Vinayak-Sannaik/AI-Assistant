from src.retrieval.reranker import Reranker

reranker = Reranker()

query = "Why is ChromaDB useful?"

documents = [
    "ChromaDB is a vector database.",
    "ChromaDB is useful because it stores vector embeddings.",
    "FastAPI is a Python framework.",
]

results = reranker.rerank(
    query,
    documents,
)

for doc, score in results:
    print("\nScore:", score)
    print(doc)