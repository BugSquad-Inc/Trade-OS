from pydantic import BaseModel
from typing import Optional

class OutreachRequest(BaseModel):
    buyer_id: str
    tone: str = "Professional"
    contact_name: Optional[str] = None

class OutreachResponse(BaseModel):
    action_id: str
    buyer_id: str
    buyer_name: str
    contact_name: str
    contact_title: str
    tone: str
    subject: str
    body: str
    status: str
