# from src.ingestion.document_loader import DocumentLoader

from src.ingestion.document_loader import DocumentLoader

loader = DocumentLoader()

documents = loader.load("data/sample.txt")

print(f"Loaded {len(documents)} documents")

for doc in documents:
    print(doc.page_content)