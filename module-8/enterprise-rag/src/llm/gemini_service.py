from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import GOOGLE_API_KEY


class GeminiService:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0,
        )

    def invoke(self, prompt: str):
        response = self.llm.invoke(prompt)

        return response.content