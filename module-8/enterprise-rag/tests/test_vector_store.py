from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker
from src.retrieval.vector_store import VectorStore

loader = DocumentLoader()
chunker = TextChunker()
vector_store = VectorStore()

documents = loader.load("data/sample.txt")
chunks = chunker.split_documents(documents)

vector_store.add_documents(chunks)

print("Indexed successfully")