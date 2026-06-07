import chromadb
import uuid

from src.embeddings.embedding_service import EmbeddingService


# class ChromaEmbeddingFunction:
#     def __init__(self):
#         self.embedding_service = EmbeddingService()

#     def __call__(self, input):
#         return self.embedding_service.model.encode(input).tolist()

#     def name(self):
#         return "bge-small-en-v1.5"


class VectorStore:

    def __init__(self):
        self.embedding_service = EmbeddingService()

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
        )

    def count(self):
        return self.collection.count()

    def add_documents(self, documents):

        texts = [
            doc.page_content
            for doc in documents
        ]

        embeddings = self.embedding_service.embed_documents(
            documents
        )

        self.collection.add(
            ids=[
                str(uuid.uuid4())
                for _ in documents
            ],
            documents=texts,
            embeddings=embeddings,
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
    
    def reset(self):
        self.client.delete_collection("documents")

        self.collection = self.client.get_or_create_collection(
            name="documents",
            # embedding_function=ChromaEmbeddingFunction(),
        )