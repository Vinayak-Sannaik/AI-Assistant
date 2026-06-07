from src.ingestion.document_loader import DocumentLoader
from src.ingestion.text_chunker import TextChunker

loader = DocumentLoader()
chunker = TextChunker(
    chunk_size=100,
    chunk_overlap=20,
)

documents = loader.load("data/sample.txt")

chunks = chunker.split_documents(documents)

print(f"Total chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print("\n----------------")
    print(f"Chunk {i + 1}")
    print(chunk.page_content)
    print(chunks[0])
    print(chunks[0].metadata)

