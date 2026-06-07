from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker
from src.retrieval.bm25_retriever import BM25Retriever

loader = DocumentLoader()

# chunker = TextChunker()

chunker = TextChunker(
    chunk_size=80,
    chunk_overlap=10
)

documents = loader.load(
    "data/sample.txt"
)

chunks = chunker.split_documents(
    documents
)

retriever = BM25Retriever()

retriever.index(chunks)

results = retriever.search(
    "ChromaDB",
    top_k=3,
)

for doc, score in results:
    print("\nScore:", score)
    print(doc.page_content)