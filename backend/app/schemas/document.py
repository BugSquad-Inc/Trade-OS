import uuid
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.document import DocumentType, ShipmentMilestone

class TradeDocumentBase(BaseModel):
    opportunity_id: Optional[uuid.UUID] = None
    shipment_id: Optional[uuid.UUID] = None
    product_version_id: Optional[uuid.UUID] = None
    doc_type: DocumentType
    title: str
    file_name: str
    file_size_bytes: int = 102400
    file_hash_sha256: str = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    mime_type: str = "application/pdf"
    storage_uri: str = "s3://tradeos-vault/docs/sample.pdf"
    status: str = "verified"
    metadata_json: Dict[str, Any] = Field(default_factory=dict)

class TradeDocumentCreate(TradeDocumentBase):
    pass

class TradeDocumentResponse(TradeDocumentBase):
    id: uuid.UUID
    tenant_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ComplianceAuditRequest(BaseModel):
    product_version_id: Optional[uuid.UUID] = None
    exporter_certs: List[str] = Field(default_factory=lambda: ["LWG Gold Rated", "ISO 14001:2015", "REACH SVHC Tested"])
    has_farm_polygons: bool = True
    cr_vi_tested_zero: bool = True
    reach_svhc_zero: bool = True

class ComplianceCheckItem(BaseModel):
    regulation: str
    requirement: str
    passed: bool
    weight: int
    evidence: str

class ComplianceAuditResponse(BaseModel):
    overall_score: int
    clearance_grade: str
    status: str
    checks: List[ComplianceCheckItem]
    remediation_actions: List[str]
    audited_at: str
    auditor: str

class ShipmentBase(BaseModel):
    opportunity_id: Optional[uuid.UUID] = None
    buyer_id: uuid.UUID
    container_number: str = "MSKU1234567"
    vessel_name: str = "Maersk Mc-Kinney Moller"
    voyage_number: str = "2608W"
    carrier: str = "Maersk Line"
    origin_port: str = "Chennai Port (INMAA)"
    destination_port: str = "Hamburg Port (DEHAM)"
    etd: date
    eta: date
    milestone: ShipmentMilestone = ShipmentMilestone.vessel_departed
    tracking_status: str = "on_time"
    gross_weight_kg: float = 14500.0
    invoice_amount_usd: float = 45000.0
    realized_amount_inr: float = 0.0
    ebrc_status: str = "pending"
    ebrc_number: Optional[str] = None

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentMilestoneUpdate(BaseModel):
    milestone: ShipmentMilestone
    tracking_status: Optional[str] = None
    ebrc_status: Optional[str] = None
    realized_amount_inr: Optional[float] = None

class ShipmentResponse(ShipmentBase):
    id: uuid.UUID
    tenant_id: Optional[uuid.UUID] = None
    shipment_ref: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
