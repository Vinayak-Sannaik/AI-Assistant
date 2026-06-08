from langchain_groq import ChatGroq

from src.config import GROQ_API_KEY


class GroqService:

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=GROQ_API_KEY,
            temperature=0,
        )

    def invoke(self, prompt: str):
        response = self.llm.invoke(prompt)
        return response.content