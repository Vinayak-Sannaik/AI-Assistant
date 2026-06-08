from src.llm.gemini_service import GeminiService
from src.llm.groq_service import GroqService


class LLMService:

    def __init__(self):
        self.gemini = GeminiService()
        self.groq = GroqService()

    def invoke(
        self,
        prompt: str,
    ):
        try:
           print("Using Groq...")
           return self.groq.invoke(prompt)

        except Exception as e:
            print(f"Groq failed: {e}")
            print("Falling back to Gemini...")
            return self.gemini.invoke(prompt)

            