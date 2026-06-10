from src.llm.llm_service import LLMService

class MultiHopPlanner:

    def __init__(self):
        self.llm = LLMService()

    def generate_steps(
        self,
        question: str,
    ):
        prompt = f"""
Break this question into smaller
search queries.

Question:
{question}

Return one query per line.
"""

        response = self.llm.invoke(
            prompt
        )

        return [
            line.strip()
            for line in response.split("\n")
            if line.strip()
        ]