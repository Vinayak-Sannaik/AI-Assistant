def reciprocal_rank_fusion(
    ranked_lists,
    k=60,
):
    scores = {}
    documents = {}

    for result_list in ranked_lists:

        for rank, doc in enumerate(
            result_list,
            start=1,
        ):

            key = (
                doc.source,
                doc.chunk_id,
            )

            documents[key] = doc

            scores[key] = (
                scores.get(key, 0)
                + 1 / (k + rank)
            )

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        (
            documents[key],
            score,
        )
        for key, score in ranked
    ]