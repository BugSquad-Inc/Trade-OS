import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class VerificationQueueResponse(BaseModel):
    id: uuid.UUID
    entity_id: uuid.UUID
    entity_type: str
    entity_name: str
    claim_type: str
    priority: str
    status: str
    assigned_to: Optional[str] = None
    evidence_summary: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class SignOffRequest(BaseModel):
    approved: bool = Field(..., description="True to verify claim with evidence; False to reject")
    notes: Optional[str] = Field(None, description="Analyst verification rationale / registry citation")
    reviewer: Optional[str] = "Trade OS Senior Analyst"

class CorrectionCreate(BaseModel):
    entity_id: uuid.UUID
    entity_type: str = "company"
    field_name: str
    old_value: Optional[str] = None
    new_value: str
    reason: str
    reporter_email: Optional[str] = "exporter@butlers.in"

class CorrectionResponse(BaseModel):
    id: uuid.UUID
    entity_id: uuid.UUID
    entity_type: str
    field_name: str
    old_value: Optional[str]
    new_value: str
    reason: str
    reporter_email: str
    status: str
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class EntityResolutionLinkCreate(BaseModel):
    source_entity_id: uuid.UUID
    target_entity_id: uuid.UUID
    link_type: str = "brand_subsidiary"
    confidence: float = 0.95
    evidence: Dict[str, Any] = Field(default_factory=dict)
    reviewer: Optional[str] = "Trade OS Analyst"

class EntityResolutionLinkResponse(BaseModel):
    id: uuid.UUID
    source_entity_id: uuid.UUID
    target_entity_id: uuid.UUID
    link_type: str
    confidence: float
    evidence: Dict[str, Any]
    reviewer: Optional[str]
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
