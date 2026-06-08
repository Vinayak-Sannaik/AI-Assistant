from src.retrieval.vector_store import VectorStore

vector_store = VectorStore()

results = vector_store.collection.get()

for metadata in results["metadatas"]:
    print(metadata)