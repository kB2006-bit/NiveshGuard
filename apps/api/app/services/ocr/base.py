from abc import ABC, abstractmethod
from typing import Dict, Any

class OCRProvider(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> Dict[str, Any]:
        """
        Extract text from an image/document.
        Returns a dict containing 'text' and 'confidence'.
        """
        pass
