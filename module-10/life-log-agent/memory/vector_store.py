import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "memory/faiss.index"

dimension = 384


class VectorStore:

    def __init__(self):

        try:
            self.index = faiss.read_index(INDEX_PATH)

        except:

            self.index = faiss.IndexFlatL2(dimension)

    def add(self, text):

        embedding = MODEL.encode([text])

        self.index.add(
            np.array(embedding).astype("float32")
        )

        faiss.write_index(
            self.index,
            INDEX_PATH,
        )

    def search(self, query, k=3):

        embedding = MODEL.encode([query])

        distances, indices = self.index.search(
            np.array(embedding).astype("float32"),
            k,
        )

        return indices[0]