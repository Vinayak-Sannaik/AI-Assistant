from src.retrieval.vector_store import VectorStore
from src.retrieval.reranker import Reranker

vector_store = VectorStore()
reranker = Reranker()

query = "Why is ChromaDB useful?"

results = vector_store.search(
    query,
    top_k=5
)

documents = results["documents"][0]

print("\nRetrieved Chunks")
for doc in documents:
    print("\n---")
    print(doc)

reranked = reranker.rerank(
    query,
    documents,
    top_k=5
)

print("\nReranked Chunks")
for doc, score in reranked:
    print("\n---")
    print("Score:", score)
    print(doc)