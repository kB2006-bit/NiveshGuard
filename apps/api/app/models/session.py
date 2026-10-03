from sqlalchemy import Column, String, DateTime, JSON
from .base import Base
import datetime

class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    language = Column(String, default="en")
    mode = Column(String, default="detailed")
    input_type = Column(String)
