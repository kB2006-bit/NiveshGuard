from .factory import get_ai_provider
from typing import Dict, Any

class ManipulationEngine:
    def __init__(self):
        self.ai = get_ai_provider()

    async def detect_patterns(self, text: str, extracted_claims: list) -> Dict[str, Any]:
        prompt = (
            "Analyze the following financial text and extracted claims for manipulation patterns. "
            "Look for: Authority Signalling, Urgency/Scarcity, Guaranteed-Outcome Framing, and Social Proof. "
            "Explain why each detected pattern matters for investor safety. "
            "Remember: These are indicators of pressure, not definitive proof of fraud."
        )
        
        schema = {
            "signals": [
                {
                    "pattern": "string",
                    "evidence_span": "string",
                    "explanation": "string",
                    "severity": "low | medium | high"
                }
            ]
        }
        
        # We pass the raw text and the already extracted claims for better context
        context_prompt = f"{prompt}\n\nOriginal Text: {text}\n\nExtracted Claims: {extracted_claims}"
        return await self.ai.generate_structured_output(context_prompt, schema)

manipulation_engine = ManipulationEngine()
