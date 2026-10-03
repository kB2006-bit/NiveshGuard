import pytesseract
from PIL import Image
from .base import OCRProvider
from typing import Dict, Any
import logging

class TesseractProvider(OCRProvider):
    def __init__(self, tesseract_cmd: str = None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, file_path: str) -> Dict[str, Any]:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return {
                "text": text.strip(),
                "confidence": 0.8, 
                "provider": "tesseract"
            }
        except Exception as e:
            logging.error(f"Tesseract OCR error: {str(e)}")
            raise RuntimeError(f"OCR failed: {str(e)}")
