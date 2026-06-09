from src.retrieval.bm25_retriever import BM25Retriever

bm25 = BM25Retriever()

bm25.load_from_disk()

results = bm25.search(
    "What is ChromaDB?"
)

for doc, score in results:
    print(score)
    print(doc)

# for doc, score in results:
#     print("\nScore:", score)
#     print(doc.page_content)