from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker
from src.retrieval.vector_store import VectorStore

loader = DocumentLoader()
chunker = TextChunker(
    chunk_size=80,
    chunk_overlap=10,
)

vector_store = VectorStore()

documents = loader.load(
    "data/sample.txt"
)

chunks = chunker.split_documents(
    documents
)

# Indexing start clean
vector_store = VectorStore()

vector_store.reset()

vector_store.add_documents(
    chunks
)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}")
    print(chunk.page_content)

print("Indexed:", len(chunks))