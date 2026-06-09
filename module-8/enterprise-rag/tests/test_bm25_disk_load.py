from src.retrieval.bm25_retriever import BM25Retriever

bm25 = BM25Retriever()

bm25.load_from_disk()

results = bm25.search(
    "Module 7"
)

for doc, score in results:
    print("\nScore:", score)
    print(doc.page_content)