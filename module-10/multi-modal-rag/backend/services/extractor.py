from pypdf import PdfReader
from PIL import Image

import pytesseract
import whisper


whisper_model = whisper.load_model("base")


def extract_pdf(path: str) -> str:

    pdf = PdfReader(path)

    text = ""

    for page in pdf.pages:

        content = page.extract_text()

        if content:
            text += content + "\n"

    return text


def extract_image(path: str) -> str:

    image = Image.open(path)

    return pytesseract.image_to_string(image)


def extract_audio(path: str) -> str:

    result = whisper_model.transcribe(path)

    return result["text"]