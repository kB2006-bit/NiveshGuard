from sqlalchemy.orm import Session
from apps.api.app.models.verification import VerificationSource
from .registry import VerificationRegistryService

class VerificationMapper:
    def __init__(self):
        # Simple mapping of keywords in claims to source IDs
        # In a production system, this could be powered by an LLM or more complex logic
        self.keyword_map = {
            "sebi": "sebi_reg",
            "license": "sebi_reg",
            "registration": "sebi_reg",
            "rbi": "rbi_reg",
            "bank": "rbi_reg",
            "nbfc": "rbi_reg",
            "cybercrime": "cybercrime_gov",
            "police": "cybercrime_gov",
            "reporting": "cybercrime_gov",
            "whatsapp": "chakshu_sanchar",
            "sms": "chakshu_sanchar",
            "call": "chakshu_sanchar",
            "number": "chakshu_sanchar"
        }

    def map_claims_to_sources(self, db: Session, claims: list):
        """
        Maps a list of claims to authoritative sources.
        Each claim result includes the source and specific instructions.
        """
        results = []
        registry_service = VerificationRegistryService()

        for claim in claims:
            claim_text = claim.lower()
            matched_source_id = None

            # Match keywords to source IDs
            for keyword, source_id in self.keyword_map.items():
                if keyword in claim_text:
                    matched_source_id = source_id
                    break

            if matched_source_id:
                source = registry_service.get_source_by_id(db, matched_source_id)
                if source and source.is_active:
                    results.append({
                        "claim": claim,
                        "source": {
                            "source_id": source.source_id,
                            "entity_name": source.entity_name,
                            "official_url": source.official_url,
                            "instructions": source.verification_instructions
                        },
                        "status": "verifiable"
                    })
                    continue

            # Default for unmapped claims: recommend independent manual verification
            results.append({
                "claim": claim,
                "status": "manual_verification_required",
                "instructions": "This claim could not be automatically mapped to a registry source. Please verify this independently via official channels."
            })

        return results
