from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    wa_id: str
    content: str
    timestamp: str
    status: str
