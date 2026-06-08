from src.llm.llm_service import LLMService

llm = LLMService()

response = llm.invoke(
    "What is ChromaDB?"
)

print(response)