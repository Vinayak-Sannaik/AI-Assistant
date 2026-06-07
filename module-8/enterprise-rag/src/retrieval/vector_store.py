import chromadb

from src.embeddings.embedding_service import EmbeddingService


class ChromaEmbeddingFunction:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def __call__(self, input):
        return self.embedding_service.model.encode(input).tolist()

    def name(self):
        return "bge-small-en-v1.5"


class VectorStore:

    def __init__(self):
        self.embedding_service = EmbeddingService()
        
        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=ChromaEmbeddingFunction(),
        )

    def add_documents(self, documents):
        self.collection.add(
            ids=[
                f"chunk_{i}"
                for i in range(len(documents))
            ],
            documents=[
                doc.page_content
                for doc in documents
            ],
            metadatas=[
                doc.metadata
                for doc in documents
            ],
        )

    def search(self, query: str, top_k: int = 3):
        query_embedding = self.embedding_service.embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        return results