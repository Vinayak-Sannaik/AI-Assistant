from src.llm.gemini_service import GeminiService


class QueryRewriter:

    def __init__(self):
        self.llm = GeminiService()

    def rewrite(
        self,
        question: str,
        conversation_history: str,
    ):
        prompt = f"""
            You are a query rewriting assistant.

            Your task is to convert a follow-up question into a standalone question.

            Conversation:
            {conversation_history}

            Question:
            {question}

            Return only the rewritten standalone question.
            Do not explain anything.
            """

        return self.llm.invoke(prompt).strip()