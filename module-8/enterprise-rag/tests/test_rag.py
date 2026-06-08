from src.retrieval.rag_service import RAGService

rag = RAGService()

# response = rag.ask(
#     "What is ChromaDB?"
# )
# response = rag.ask(
#     "Who invented Python?"
# )
response = rag.ask(
    "Why is ChromaDB useful?"
)

print(response)