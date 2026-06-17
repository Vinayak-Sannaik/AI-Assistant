from sentence_transformers import (
    CrossEncoder
)

reranker = CrossEncoder(
    "BAAI/bge-reranker-base"
)

def rerank(
    query,
    docs
):

    pairs = [
        [query, doc]
        for doc in docs
    ]

    scores = reranker.predict(
        pairs
    )

    ranked = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [x[0] for x in ranked[:5]]