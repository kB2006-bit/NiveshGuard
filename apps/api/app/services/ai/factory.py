from .ollama import OllamaProvider
from .base import AIProvider

def get_ai_provider() -> AIProvider:
    # Default to Ollama as per approved decisions
    return OllamaProvider()
