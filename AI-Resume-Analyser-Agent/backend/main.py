import os
import pdfplumber
from docx import Document
from pdf2image import convert_from_path
import easyocr

# Initialize OCR once
reader = easyocr.Reader(['en'])

class DocumentExtractor:
    # DOCX (NO OCR)
    def extract_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


    # PDF (TEXT EXTRACTION)
    def extract_pdf_text(self, file_path: str) -> str:
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip()


    # OCR (SCANNED PDF ONLY)
    def pdf_to_images(self, file_path: str):
        return convert_from_path(file_path)


    def ocr_image(self, image) -> str:
        results = reader.readtext(image, detail=0)
        return " ".join(results)


    def extract_pdf_ocr(self, file_path: str) -> str:
        images = self.pdf_to_images(file_path)

        text = ""
        for img in images:
            text += self.ocr_image(img) + "\n"

        return text.strip()


    # SMART HANDLER (MAIN FUNCTION)
    def extract_text(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()

        # DOCX → direct extraction
        if ext == ".docx":
            return self.extract_docx(file_path)

        # PDF → try normal first
        elif ext == ".pdf":
            text = self.extract_pdf_text(file_path)

            # fallback → OCR if empty (scanned PDF)
            if not text.strip():
                text = self.extract_pdf_ocr(file_path)

            return text

        else:
            raise ValueError("Only PDF and DOCX supported")


obj = DocumentExtractor()

text = obj.extract_text("C:\\Users\\Monish. S\\OneDrive\\Desktop\\Monish Resume.pdf")

print(text)