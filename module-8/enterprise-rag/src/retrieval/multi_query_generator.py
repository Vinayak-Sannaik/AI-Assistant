from src.llm.gemini_service import GeminiService


class MultiQueryGenerator:

    def __init__(self):
        self.llm = GeminiService()

    def generate(self, question: str):

        prompt = f"""
Generate 4 different search queries.

The queries should help retrieve relevant
documents from a vector database.

Question:
{question}

Return one query per line.
Do not number them.
"""

        response = self.llm.invoke(prompt)

        return [
            line.strip()
            for line in response.split("\n")
            if line.strip()
        ]