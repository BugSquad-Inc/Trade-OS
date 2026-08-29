import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.audit import AuditCategory

class AuditEventCreate(BaseModel):
    tenant_id: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    event_category: AuditCategory = AuditCategory.MODIFICATION
    action: str
    entity_type: str
    entity_id: Optional[uuid.UUID] = None
    actor_email: str = "system@tradeos.in"
    ip_address: str = "127.0.0.1"
    user_agent: str = "TradeOS-Client/2.0"
    payload_diff: Dict[str, Any] = Field(default_factory=dict)

class AuditEventResponse(AuditEventCreate):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}

class AuditStatsResponse(BaseModel):
    total_audit_events: int
    compliance_sign_offs: int
    financial_modifications: int
    security_access_events: int
    tamper_evident_status: str
