import pdfplumber
from extraction.ocr import ocr_image, ocr_pdf

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"

        if len(text.strip()) > 200:
            return text, "pdf_text"

        return ocr_pdf(file_path), "pdf_ocr"

    return ocr_image(file_path), "image_ocr"
