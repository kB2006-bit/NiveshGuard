from .tesseract import TesseractProvider
from .base import OCRProvider

def get_ocr_provider() -> OCRProvider:
    return TesseractProvider()
