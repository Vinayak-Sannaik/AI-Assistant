from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker
from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever

loader = DocumentLoader()

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

vector_store = VectorStore()

vector_store.add_documents(
    chunks
)

bm25 = BM25Retriever()

bm25.index(
    chunks
)

hybrid = HybridRetriever(
    vector_store,
    bm25
)

results = hybrid.search(
    "ChromaDB"
)

# for result in results:
#     print("\n---")
#     print(result)
    # print("Chunk Count:", len(chunks))
    # print("Chroma Count:", vector_store.collection.count())