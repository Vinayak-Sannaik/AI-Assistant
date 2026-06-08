from src.retrieval.vector_store import VectorStore
from src.retrieval.bm25_retriever import BM25Retriever
from src.retrieval.hybrid_retriever import HybridRetriever


vector_store = VectorStore()

bm25 = BM25Retriever()
bm25.load_from_disk()

hybrid = HybridRetriever(
    vector_store,
    bm25,
)

results = hybrid.search(
    query="What is RAG?",
    source="data/sample.md",
)

for result in results:
    print("\n---")
    print(result)