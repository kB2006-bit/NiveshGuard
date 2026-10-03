from .factory import get_ai_provider
from typing import Dict, Any

class ExtractionService:
    def __init__(self):
        self.ai = get_ai_provider()

    async def extract_claims_and_entities(self, text: str) -> Dict[str, Any]:
        prompt = (
            "You are a financial safety analyst. Analyze the following text from a financial communication. "
            "Extract all specific financial promises, return claims, authority signals, and requested actions. "
            "For every item, identify the exact supporting text (span) from the original content. "
            "Do not invent information. If a claim is vague, mark it as such."
        )
        
        schema = {
            "claims": [
                {
                    "claim": "string", 
                    "evidence_span": "string", 
                    "category": "return_promise | authority_claim | requested_action | urgency",
                    "confidence": "float"
                }
            ],
            "entities": [
                {
                    "name": "string",
                    "type": "company | person | regulator | url | phone",
                    "evidence_span": "string"
                }
            ]
        }
        
        return await self.ai.generate_structured_output(prompt, schema)

extraction_service = ExtractionService()
