from src.llm.groq_service import GroqService

llm = GroqService()

response = llm.invoke(
    "What is ChromaDB?"
)

print(response)