import secrets
from datetime import datetime, timedelta
from typing import Dict
from .config import settings

# Simple ephemeral session store for MVP
# In production, this would be in Redis
session_store: Dict[str, dict] = {}

def create_session() -> str:
    session_id = secrets.token_urlsafe(32)
    session_store[session_id] = {
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(hours=2)
    }
    return session_id

def get_session(session_id: str):
    session = session_store.get(session_id)
    if session and session["expires_at"] > datetime.utcnow():
        return session
    return None
