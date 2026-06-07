from src.retrieval.rrf import (
    reciprocal_rank_fusion
)

bm25 = [
    "chunk_a",
    "chunk_b",
    "chunk_c",
]

vector = [
    "chunk_b",
    "chunk_a",
    "chunk_d",
]

results = reciprocal_rank_fusion(
    [bm25, vector]
)

for item, score in results:
    print(item, score)