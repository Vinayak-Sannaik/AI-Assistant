from src.retrieval.vector_store import VectorStore

vector_store = VectorStore()



results = vector_store.search(
    # "ChromaDB",
    # top_k=5
    "What is ChromaDB?"
)

# print(results["documents"][0])
# print(results["distances"][0])

for doc in results:
    print(doc)