from src.llm.llm_service import LLMService


class MultiQueryGenerator:

    def __init__(self):
        self.llm = LLMService()

    def generate(
        self,
        question: str,
    ):

        prompt = f"""
            You are helping a retrieval system.

            Generate 4 alternative search queries that
            could retrieve relevant documents for the
            same user intent.

            Question:
            {question}

            Requirements:
            - Different wording
            - Different keywords
            - Same meaning
            - One query per line
            - No numbering
            """

        response = self.llm.invoke(
            prompt
        )

        queries = [
            line.strip()
            for line in response.split("\n")
            if line.strip()
        ]

        return queries