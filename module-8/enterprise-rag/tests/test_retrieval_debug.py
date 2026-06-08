from src.retrieval.retrieval_pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()

result = pipeline.retrieve(
    "Why is ChromaDB useful?"
)

for chunk, score in zip(
    result["chunks"],
    result["scores"]
):
    print("\n---")
    print("Score:", score)
    print(chunk)