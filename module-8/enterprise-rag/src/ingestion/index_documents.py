import json

from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker
from src.retrieval.vector_store import VectorStore


def index_documents():

    loader = DocumentLoader()

    chunker = TextChunker(
        chunk_size=80,
        chunk_overlap=10,
    )

    documents = loader.load_directory(
        "data"
    )

    chunks = chunker.split_documents(
        documents
    )

    # Save chunks for BM25 rebuilding
    chunk_data = [
        {
            "content": chunk.page_content,
            "metadata": chunk.metadata,
        }
        for chunk in chunks
    ]

    with open(
        "data/chunks.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            chunk_data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    vector_store = VectorStore()

    vector_store.reset()

    vector_store.add_documents(
        chunks
    )

    print(
        f"Indexed: {len(chunks)}"
    )

    print(
        "Saved chunks to: data/chunks.json"
    )

    return len(chunks)


if __name__ == "__main__":
    index_documents()