import chromadb
import uuid

from src.embeddings.embedding_service import EmbeddingService
from src.retrieval.retrieval_document import RetrievalDocument


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

    def search(
        self,
        query: str,
        top_k: int = 3,
        source: str | None = None,
    ):
        query_embedding = self.embedding_service.embed_text(query)

        query_params = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
        }

        if source:
            query_params["where"] = {
                "source": source
            }

        self.collection = self.client.get_or_create_collection(
            name="documents",
        )

        results = self.collection.query(
            **query_params
        )

        documents = []

        for content, metadata in zip(
            results["documents"][0],
            results["metadatas"][0],
        ):
            documents.append(
                RetrievalDocument(
                    content=content,
                    source=metadata.get(
                        "source",
                        "Unknown",
                    ),
                    chunk_id=metadata.get(
                        "chunk_id"
                    ),
                )
            )

        return documents
    
    def reset(self):
        self.client.delete_collection("documents")

        self.collection = self.client.get_or_create_collection(
            name="documents",
        )