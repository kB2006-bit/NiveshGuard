from sqlalchemy import Column, String, Boolean, DateTime, Integer
from .base import Base
import datetime

class VerificationSource(Base):
    __tablename__ = "verification_sources"
    source_id = Column(String, primary_key=True, index=True)
    entity_name = Column(String, nullable=False)
    category = Column(String) # e.g., 'Regulator', 'Bank', 'Police'
    official_url = Column(String, nullable=False)
    verification_instructions = Column(String)
    is_active = Column(Boolean, default=True)
    version = Column(String, default="1.0")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
