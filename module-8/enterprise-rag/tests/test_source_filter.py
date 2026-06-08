from src.retrieval.vector_store import VectorStore

vector_store = VectorStore()

results = vector_store.search(
    query="What is RAG?",
    source="data/sample.md",
)

print(results["documents"][0])