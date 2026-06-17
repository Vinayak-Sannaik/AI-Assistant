from rank_bm25 import BM25Okapi

class BM25Retriever:

    def __init__(self, chunks):

        self.chunks = chunks

        self.tokenized = [
            chunk.split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(
            self.tokenized
        )

    def search(self, query):

        scores = self.bm25.get_scores(
            query.split()
        )

        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:5]