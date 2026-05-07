import os
import io
import pdfplumber
from docx import Document
from pdf2image import convert_from_bytes
import easyocr
from PIL import Image

reader = easyocr.Reader(['en'], gpu=False)


class DocumentExtractor:

    def __init__(self, file_bytes: bytes, filename: str):
        self.file_bytes = file_bytes
        self.filename = filename
        self.ext = os.path.splitext(filename)[1].lower()

    def extract(self) -> str:
        if self.ext == ".docx":
            return self._extract_docx()

        elif self.ext == ".pdf":
            text = self._extract_pdf_text()
            if not text.strip():
                text = self._extract_pdf_ocr()
            return text

        elif self.ext in [".png", ".jpg", ".jpeg"]:
            return self._extract_image()

        else:
            raise ValueError("Unsupported file type")

    def _extract_docx(self):
        doc = Document(io.BytesIO(self.file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    def _extract_pdf_text(self):
        text = ""
        with pdfplumber.open(io.BytesIO(self.file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        return text.strip()

    def _extract_pdf_ocr(self):
        images = convert_from_bytes(self.file_bytes)
        text = ""
        for img in images:
            text += " ".join(reader.readtext(img, detail=0)) + "\n"
        return text.strip()

    def _extract_image(self):
        image = Image.open(io.BytesIO(self.file_bytes))
        return " ".join(reader.readtext(image, detail=0))