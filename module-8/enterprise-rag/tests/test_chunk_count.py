from src.retrieval.vector_store import VectorStore

vector_store = VectorStore()

print("Count:", vector_store.collection.count())
print(vector_store.count())