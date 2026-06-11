class ContextCompressor:

    def __init__(self, model):
        self.model = model

    def compress(
        self,
        query: str,
        documents: list[dict],
        top_sentences: int = 2,
    ):

        compressed_documents = []

        for document in documents:

            content = document["content"]

            # Skip small chunks
            if len(content) < 500:
                compressed_documents.append(
                    document
                )
                continue

            sentences = [
                sentence.strip()
                for sentence in content.split(".")
                if sentence.strip()
            ]

            if len(sentences) <= 2:
                compressed_documents.append(
                    document
                )
                continue

            pairs = [
                [query, sentence]
                for sentence in sentences
            ]

            scores = self.model.predict(
                pairs
            )

            ranked = sorted(
                zip(sentences, scores),
                key=lambda x: x[1],
                reverse=True,
            )

            compressed_text = ". ".join(
                sentence
                for sentence, _score in ranked[
                    :top_sentences
                ]
            )

            compressed_documents.append(
                {
                    **document,
                    "content": compressed_text,
                }
            )

        return compressed_documents