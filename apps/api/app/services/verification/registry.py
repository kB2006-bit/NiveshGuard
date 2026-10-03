from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from apps.api.app.models.verification import VerificationSource
import uuid
import uuid

class VerificationRegistryService:
    def __init__(self):
        # Core seed data for the hackathon MVP
        self.seed_data = [
            {
                "source_id": "sebi_reg",
                "entity_name": "SEBI (Securities and Exchange Board of India)",
                "category": "Regulator",
                "official_url": "https://www.sebi.gov.in",
                "verification_instructions": "Check the 'Registered Intermediaries' section on the official SEBI website to verify the license of the investment advisor or broker."
            },
            {
                "source_id": "rbi_reg",
                "entity_name": "RBI (Reserve Bank of India)",
                "category": "Regulator",
                "official_url": "https://www.rbi.org.in",
                "verification_instructions": "Verify the NBFC or Bank registration via the RBI official list of regulated entities."
            },
            {
                "source_id": "cybercrime_gov",
                "entity_name": "National Cyber Crime Reporting Portal",
                "category": "Police",
                "official_url": "https://cybercrime.gov.in",
                "verification_instructions": "Report suspicious financial activity or verify reported scam patterns on the official government portal."
            },
            {
                "source_id": "chakshu_sanchar",
                "entity_name": "Chakshu (Sanchar Saathi)",
                "category": "Regulator",
                "official_url": "https://sancharsaathi.gov.in",
                "verification_instructions": "Report fraudulent communications or verify reported spam numbers via the Chakshu facility."
            }
        ]

    def seed_registry(self, db: Session):
        """Populates the registry if empty."""
        existing = db.query(VerificationSource).first()
        if not existing:
            for data in self.seed_data:
                source = VerificationSource(**data)
                db.add(source)
            db.commit()

    def get_active_sources(self, db: Session):
        return db.query(VerificationSource).filter(VerificationSource.is_active == True).all()

    def get_source_by_id(self, db: Session, source_id: str):
        return db.query(VerificationSource).filter(VerificationSource.source_id == source_id).first()

    def list_sources(self, db: Session):
        return self.get_active_sources(db)
