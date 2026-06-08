from src.retrieval.retrieval_pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()

results = pipeline.retrieve(
    "Why is ChromaDB useful?"
)

for result in results:
    print("\n---")
    print(result)