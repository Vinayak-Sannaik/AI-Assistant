from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker
from src.retrieval.vector_store import VectorStore

loader = DocumentLoader()
chunker = TextChunker()
vector_store = VectorStore()

documents = loader.load("data/sample.txt")
chunks = chunker.split_documents(documents)

# Optional during development
# vector_store.collection.delete(...)

vector_store.add_documents(chunks)

results = vector_store.search(
    "What is a vector database?",
    top_k=3,
)

print(results["documents"][0])
print("Results:",results)