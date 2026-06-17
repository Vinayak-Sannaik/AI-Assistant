from pathlib import Path
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from services.extractor import (
    extract_pdf,
    extract_image,
    extract_audio
)

from services.chunker import chunk_text
from services.vector_store import add_chunks

router = APIRouter()

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    exist_ok=True
)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    file_path = (
        UPLOAD_DIR /
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":

        text = extract_pdf(
            str(file_path)
        )

    elif suffix in [
        ".png",
        ".jpg",
        ".jpeg"
    ]:

        text = extract_image(
            str(file_path)
        )

    elif suffix in [
        ".mp3",
        ".wav",
        ".m4a"
    ]:

        text = extract_audio(
            str(file_path)
        )

    else:

        return {
            "error": "Unsupported file type"
        }

    chunks = chunk_text(text)

    add_chunks(chunks)

    return {
        "message": "File indexed",
        "chunks": len(chunks)
    }