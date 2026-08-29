import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.provenance import TruthStatus, SourceTier

class SourceRegistryBase(BaseModel):
    name: str = Field(..., description="Name of the data source")
    source_tier: SourceTier = Field(default=SourceTier.tier_e, description="Data source tier classification")
    licence_terms: Optional[str] = Field(None, description="Licence or usage rights agreement summary")
    usage_policy: Optional[str] = Field(None, description="Permitted customer-facing use basis")
    owner: str = Field(default="Trade OS Data Operations", description="Internal owner responsible for source freshness")
    is_active: bool = True

class SourceRegistryCreate(SourceRegistryBase):
    pass

class SourceRegistryResponse(SourceRegistryBase):
    id: uuid.UUID
    checked_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class EvidenceAssertionBase(BaseModel):
    claim_type: str = Field(..., description="Type of assertion e.g. buyer_interest, certification, contact_role")
    claim_value: Dict[str, Any] = Field(..., description="Structured assertion payload")
    truth_status: TruthStatus = Field(default=TruthStatus.demo, description="Current truth status")
    source_id: Optional[uuid.UUID] = Field(None, description="Reference to source registry")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score from 0.0 to 1.0")
    verification_method: Optional[str] = None
    reviewed_by: Optional[str] = None
    tenant_id: Optional[uuid.UUID] = None
    metadata_info: Dict[str, Any] = Field(default_factory=dict)
    valid_from: datetime
    valid_until: Optional[datetime] = None

class EvidenceAssertionCreate(EvidenceAssertionBase):
    pass

class EvidenceAssertionResponse(EvidenceAssertionBase):
    id: uuid.UUID
    checked_at: datetime
    created_at: datetime
    source: Optional[SourceRegistryResponse] = None

    class Config:
        from_attributes = True
