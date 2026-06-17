def reciprocal_rank_fusion(
    vector_docs,
    bm25_docs,
    k=60
):
    scores = {}

    for rank, doc in enumerate(vector_docs):
        scores[doc] = scores.get(doc, 0) + 1/(rank+k)

    for rank, doc in enumerate(bm25_docs):
        scores[doc] = scores.get(doc, 0) + 1/(rank+k)

    return sorted(
        scores,
        key=scores.get,
        reverse=True
    )