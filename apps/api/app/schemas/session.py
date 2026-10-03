from pydantic import BaseModel
from typing import Optional

class SessionCreate(BaseModel):
    language: str = "en"
    mode: str = "detailed"
    input_type: str

class SessionResponse(BaseModel):
    session_id: str
    language: str
    mode: str
