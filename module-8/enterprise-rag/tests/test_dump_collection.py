from src.retrieval.vector_store import VectorStore

vector_store = VectorStore()

results = vector_store.collection.get()

print("Count:", len(results["documents"]))

for i, doc in enumerate(results["documents"]):
    print("\n---")
    print(i)
    print(doc)