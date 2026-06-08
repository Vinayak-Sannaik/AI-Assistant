from src.retrieval.retrieval_pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()

results = pipeline.retrieve(
    query="What is RAG?",
    source="data/sample.md",
)

for chunk, score in zip(
    results["chunks"],
    results["scores"],
):
    print("\n---")
    print("Score:", score)
    print(chunk)