from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker
from src.embeddings.embedding_service import EmbeddingService

loader = DocumentLoader()
chunker = TextChunker()
embedding_service = EmbeddingService()

documents = loader.load("data/sample.txt")

chunks = chunker.split_documents(documents)

embeddings = embedding_service.embed_documents(chunks)

print(f"Chunks: {len(chunks)}")
print(f"Embeddings: {len(embeddings)}")
print(f"Vector Dimension: {len(embeddings[0])}")
print(type(embeddings))
print(type(embeddings[0]))
print(len(embeddings[0]))


# Chunks: 1
# Embeddings: 1
# Vector Dimension: 384
# <class 'list'>
# <class 'list'>
# 384