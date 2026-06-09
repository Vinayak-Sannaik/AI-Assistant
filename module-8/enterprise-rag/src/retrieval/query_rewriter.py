# from src.llm.gemini_service import GeminiService
from src.llm.llm_service import LLMService

class QueryRewriter:

    def __init__(self):
        self.llm = LLMService()

    def rewrite(
        self,
        question: str,
        conversation_history,
    ):

        if not conversation_history:
            return question

        history_text = "\n".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_history
            ]
        )

        prompt = f"""
You are a query rewriting assistant.

Convert follow-up questions into standalone questions.

Conversation:
{history_text}

Question:
{question}

Return only the standalone question.
"""

        return self.llm.invoke(prompt).strip()