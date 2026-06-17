from pathlib import Path

from services.extractor import (
    extract_pdf,
    extract_image,
    extract_audio
)

from services.chunker import chunk_text
from services.vector_store import add_chunks


PDF_DIR = Path(
    "data/pdfs"
)

IMAGE_DIR = Path(
    "data/images"
)

AUDIO_DIR = Path(
    "data/audio"
)


def process_pdfs():

    for pdf in PDF_DIR.glob(
        "*.pdf"
    ):

        print(
            f"Processing {pdf.name}"
        )

        text = extract_pdf(
            str(pdf)
        )

        chunks = chunk_text(
            text
        )

        add_chunks(chunks, pdf.name)

        print(
            f"Indexed {len(chunks)} chunks"
        )


def process_images():

    for image in IMAGE_DIR.iterdir():

        if image.suffix.lower() not in [
            ".png",
            ".jpg",
            ".jpeg"
        ]:
            continue

        print(
            f"Processing {image.name}"
        )

        text = extract_image(
            str(image)
        )

        print("TEXT-----",text)

        chunks = chunk_text(
            text
        )

        print("CHUNKS-----",chunks)

        add_chunks(chunks, image.name)

        print(
            f"Indexed {len(chunks)} chunks"
        )


def process_audio():

    for audio in AUDIO_DIR.iterdir():

        if audio.suffix.lower() not in [
            ".mp3",
            ".wav",
            ".m4a"
        ]:
            continue

        print(
            f"Processing {audio.name}"
        )

        text = extract_audio(
            str(audio)
        )

        chunks = chunk_text(
            text
        )

        print("Audio chunks-----",chunks)

        add_chunks(chunks, audio.name)

        print(
            f"Indexed {len(chunks)} chunks"
        )


if __name__ == "__main__":

    process_pdfs()

    process_images()

    process_audio()

    print(
        "Indexing completed"
    )