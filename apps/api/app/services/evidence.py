from sqlalchemy.orm import Session
from ..models.evidence import EvidencePack, EvidenceItem
import uuid
import datetime

class EvidenceService:
    def create_evidence_pack(self, db: Session, incident_id: str, description: str = None):
        pack = EvidencePack(
            pack_id=str(uuid.uuid4()),
            incident_id=incident_id,
            description=description,
            created_at=datetime.datetime.utcnow()
        )
        db.add(pack)
        db.commit()
        db.refresh(pack)
        return pack

    def add_evidence_item(self, db: Session, pack_id: str, file_name: str, file_path: str, file_type: str, metadata: str = None):
        item = EvidenceItem(
            item_id=str(uuid.uuid4()),
            pack_id=pack_id,
            file_name=file_name,
            file_path=file_path,
            file_type=file_type,
            metadata_json=metadata
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_evidence_pack(self, db: Session, pack_id: str):
        return db.query(EvidencePack).filter(EvidencePack.pack_id == pack_id).first()

    def get_evidence_items(self, db: Session, pack_id: str):
        return db.query(EvidenceItem).filter(EvidenceItem.pack_id == pack_id).all()

    def get_packs_for_incident(self, db: Session, incident_id: str):
        return db.query(EvidencePack).filter(EvidencePack.incident_id == incident_id).all()
