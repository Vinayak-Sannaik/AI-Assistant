print("START")

from src.ingestion.document_loader import DocumentLoader

print("IMPORT OK")

loader = DocumentLoader()

print("LOADER OK")

documents = loader.load_directory(
    "data"
)

print("LOAD OK")
# print("Documents:", documents)

print("Documents:", len(documents))

print("Documents Count:", len(documents))

for i, doc in enumerate(documents):
    print("\n---")
    print("Index:", i)
    print("Source:", doc.metadata.get("source"))
    print("Content:", doc.page_content[:50])