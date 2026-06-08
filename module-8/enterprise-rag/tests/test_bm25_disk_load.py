from src.retrieval.bm25_retriever import BM25Retriever

bm25 = BM25Retriever()

bm25.load_from_disk()

results = bm25.search(
    "ChromaDB"
)

for doc, score in results:
    print("\nScore:", score)
    print(doc.page_content)