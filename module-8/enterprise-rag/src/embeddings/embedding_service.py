from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5"
    ):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str):
        return self.model.encode(text).tolist()

    def embed_documents(self, documents):
        texts = [doc.page_content for doc in documents]

        embeddings = self.model.encode(texts)

        return embeddings.tolist()