import os
import shutil
import uuid
from .ocr.factory import get_ocr_provider

class IntakeService:
    def __init__(self, upload_dir: str = "uploads/temp"):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
        self.ocr = get_ocr_provider()

    def process_upload(self, file, input_type: str) -> dict:
        file_ext = os.path.splitext(file.filename)[1]
        file_id = str(uuid.uuid4())
        temp_path = os.path.join(self.upload_dir, f"{file_id}{file_ext}")
        
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            if input_type == "screenshot" or input_type == "document":
                result = self.ocr.extract_text(temp_path)
                return {
                    "text": result["text"],
                    "metadata": {
                        "confidence": result["confidence"],
                        "provider": result["provider"],
                        "source": file.filename
                    }
                }
            else:
                raise ValueError(f"Unsupported input type: {input_type}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

intake_service = IntakeService()
