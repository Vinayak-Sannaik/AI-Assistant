from src.retrieval.rag_service import RAGService

rag = RAGService()

# response = rag.ask(
#     "What is ChromaDB?"
# )
response = rag.ask(
    "Who invented Python?"
)

print(response)