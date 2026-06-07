def reciprocal_rank_fusion(
    ranked_lists,
    k=60,
):
    scores = {}

    for result_list in ranked_lists:

        for rank, item in enumerate(
            result_list,
            start=1,
        ):
            scores[item] = (
                scores.get(item, 0)
                + 1 / (k + rank)
            )

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )