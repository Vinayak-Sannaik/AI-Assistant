from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from src.ingestion.index_documents import index_documents

router = APIRouter()


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    data_dir = Path("data")

    data_dir.mkdir(
        exist_ok=True
    )

    file_path = data_dir / file.filename

    with open(
        file_path,
        "wb"
    ) as buffer:
        content = await file.read()
        buffer.write(content)

    # Re-index knowledge base
    index_documents()

    return {
        "message": "Document uploaded successfully",
        "filename": file.filename,
    }