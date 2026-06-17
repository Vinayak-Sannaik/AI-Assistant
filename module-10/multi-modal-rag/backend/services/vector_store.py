from langchain_chroma import Chroma

from services.embeddings import embedding_model

COLLECTION_NAME = "multimodal"

db = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)


def add_chunks(chunks, source):
    db.add_texts(
        texts=chunks,
        ids=[str(i) for i in range(len(chunks))],
         metadata=[
            {"source": source}
            for _ in chunks
        ]
    )


def similarity_search(query: str, k: int = 4):
    return db.similarity_search(query, k=k)