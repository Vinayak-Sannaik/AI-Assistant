class QueryClassifier:

    def is_multi_hop(
        self,
        question: str,
    ):

        question = question.lower()

        indicators = [
            "why",
            "because",
            "cause",
            "impact",
            "affect",
            "relationship",
            "related",
            "depends",
            "how does",
            "how might",
            "what happens if",
        ]

        return any(
            indicator in question
            for indicator in indicators
        )