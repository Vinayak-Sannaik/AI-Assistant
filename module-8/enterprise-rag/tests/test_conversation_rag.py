from src.retrieval.rag_service import RAGService

rag = RAGService()

response1 = rag.ask(
    "What is ChromaDB?"
)

print("\nQ1:", response1)

response2 = rag.ask(
    "Why is it useful?"
)

print("\nQ2:", response2)