from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    # def split_documents(self, documents):
    #     return self.splitter.split_documents(documents)
    
    def split_documents(self, documents):
        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = index

        return chunks