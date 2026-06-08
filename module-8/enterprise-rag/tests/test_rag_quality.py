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

print("\nTop Retrieval Result")
print(documents[0])

reranked = reranker.rerank(
    query,
    documents,
    top_k=5
)

print("\nTop Reranked Result")
print(reranked[0][0])