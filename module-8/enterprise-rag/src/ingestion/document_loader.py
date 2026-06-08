from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)


class DocumentLoader:

    def load(self, file_path: str):
        path = Path(file_path)

        extension = path.suffix.lower()

        if extension == ".pdf":
            loader = PyPDFLoader(str(path))

        elif extension == ".docx":
            loader = Docx2txtLoader(str(path))

        elif extension in [".txt", ".md"]:
            loader = TextLoader(str(path), encoding="utf-8")

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return loader.load()

    def load_directory(
        self,
        directory_path: str,
    ):
        documents = []

        directory = Path(directory_path)

        supported_extensions = {
            ".pdf",
            ".docx",
            ".txt",
            ".md",
        }

        for file_path in directory.iterdir():

            if not file_path.is_file():
                continue

            if file_path.suffix.lower() not in supported_extensions:
                continue

            print("Loading:", file_path)

            docs = self.load(
                str(file_path)
            )

            documents.extend(docs)

        return documents