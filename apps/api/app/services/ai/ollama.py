import ollama
import json
import logging
from .base import AIProvider
from typing import Dict, Any
from ...core.config import settings

class OllamaProvider(AIProvider):
    def __init__(self):
        self.client = ollama.AsyncClient(host=settings.OLLAMA_BASE_URL)
        self.model = settings.OLLAMA_MODEL

    async def generate_structured_output(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Construct the prompt to force JSON output based on the schema
            full_prompt = f"{prompt}\n\nReturn the result as a JSON object following this schema: {json.dumps(schema)}"
            
            response = await self.client.generate(
                model=self.model,
                prompt=full_prompt,
                format="json",
                options={"temperature": 0} # Deterministic for extraction
            )
            
            return json.loads(response['response'])
        except Exception as e:
            logging.error(f"Ollama AI error: {str(e)}")
            raise RuntimeError(f"AI processing failed: {str(e)}")
