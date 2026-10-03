from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from .base import Base
import datetime

class EvidencePack(Base):
    __tablename__ = "evidence_packs"
    pack_id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("incidents.incident_id"), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String)

class EvidenceItem(Base):
    __tablename__ = "evidence_items"
    item_id = Column(String, primary_key=True, index=True)
    pack_id = Column(String, ForeignKey("evidence_packs.pack_id"))
    file_name = Column(String)
    file_path = Column(String)
    file_type = Column(String) # e.g., 'screenshot', 'log', 'document'
    captured_at = Column(DateTime, default=datetime.datetime.utcnow)
    metadata_json = Column(String) # Simplified JSON as string for evidence metadata
