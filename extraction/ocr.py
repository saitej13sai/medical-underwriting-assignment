import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# HARD SET FOR WINDOWS – NO PATH ISSUES
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

TESS_CONFIG = "--oem 3 --psm 6"

def ocr_image(image_path):
    img = Image.open(image_path).convert("RGB")
    return pytesseract.image_to_string(img, config=TESS_CONFIG)

def ocr_pdf(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    return "\n".join(
        pytesseract.image_to_string(p, config=TESS_CONFIG) for p in pages
    )
