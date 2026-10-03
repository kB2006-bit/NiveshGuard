from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from .base import Base
import datetime

class Incident(Base):
    __tablename__ = "incidents"
    incident_id = Column(String, primary_key=True, index=True)
    analysis_id = Column(String)
    user_id = Column(String, index=True)
    incident_date = Column(DateTime)
    user_notes = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
