import uuid
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ProductCertificateBase(BaseModel):
    cert_type: str = Field(..., description="LWG, ISO9001, REACH_TEST, CHROMIUM_VI, AZO_FREE")
    certificate_name: str
    issuer: str
    accredited_lab: Optional[str] = "Eurofins / TÜV Rheinland"
    scope: Optional[str] = None
    file_hash: Optional[str] = None
    issue_date: date
    expiry_date: Optional[date] = None
    status: str = "verified"

class ProductCertificateCreate(ProductCertificateBase):
    pass

class ProductCertificateResponse(ProductCertificateBase):
    id: uuid.UUID
    product_version_id: uuid.UUID
    verified_by: Optional[str]
    verified_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}

class ProductPassportResponse(BaseModel):
    id: uuid.UUID
    product_version_id: uuid.UUID
    passport_number: str
    status: str
    recipient_buyer_id: Optional[uuid.UUID]
    generated_at: datetime
    passport_metadata: Dict[str, Any]

    model_config = {"from_attributes": True}

class ProductVersionBase(BaseModel):
    version_tag: str = "v1.0"
    materials: List[str] = Field(default_factory=list)
    finishes: List[str] = Field(default_factory=list)
    thickness_range_mm: List[str] = Field(default_factory=list)
    monthly_capacity_sqft: int = 25000
    moq_sqft: int = 2000
    lead_time_days: int = 30
    sample_lead_time_days: int = 7
    price_basis_inr: float = 280.0
    price_basis_usd: float = 3.35
    incoterms: List[str] = Field(default_factory=lambda: ["FOB", "CIF"])
    status: str = "approved"

class ProductVersionCreate(ProductVersionBase):
    pass

class ProductVersionResponse(ProductVersionBase):
    id: uuid.UUID
    product_family_id: uuid.UUID
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    created_at: datetime
    certificates: List[ProductCertificateResponse] = Field(default_factory=list)
    passports: List[ProductPassportResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}

class ProductFamilyBase(BaseModel):
    name: str
    category: str = "Finished Leather"
    hs_code: str = "4107"
    itc_hs_code: Optional[str] = "4107.12.00"
    leather_type: str = "Bovine Full Grain"
    description: Optional[str] = None
    is_active: bool = True

class ProductFamilyCreate(ProductFamilyBase):
    materials: Optional[List[str]] = None
    finishes: Optional[List[str]] = None
    thickness_range_mm: Optional[List[str]] = None
    monthly_capacity_sqft: Optional[int] = None
    moq_sqft: Optional[int] = None
    lead_time_days: Optional[int] = None
    price_basis_inr: Optional[float] = None
    price_basis_usd: Optional[float] = None

class ProductFamilyResponse(ProductFamilyBase):
    id: uuid.UUID
    tenant_id: Optional[uuid.UUID]
    created_at: datetime
    versions: List[ProductVersionResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}
