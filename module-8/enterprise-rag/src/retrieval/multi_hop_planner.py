from src.llm.llm_service import LLMService

class MultiHopPlanner:

    def __init__(self):
        self.llm = LLMService()

    def generate_steps(
        self,
        question: str,
    ):
        prompt = f"""
Break this question into factual retrieval steps.

Question:
{question}

Rules:
- Preserve all named entities.
- Do not generate generic educational questions.
- Each step should retrieve a missing fact.
- Maximum 4 steps.

Return one step per line.
"""

        response = self.llm.invoke(
            prompt
        )

        return [
            line.strip()
            for line in response.split("\n")
            if line.strip()
        ]