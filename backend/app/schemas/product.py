import uuid
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class ProductSpecificationBase(BaseModel):
    thickness_min_mm: float = 1.2
    thickness_max_mm: float = 1.4
    temper: str = "medium_soft"
    tensile_strength_n_per_mm2: float = 15.0
    tear_strength_n: float = 40.0
    grain_type: str = "Full Grain Natural Mill"
    tannage_type: str = "Chrome-Free Synthetic / Veg Retan"
    origin_country: str = "India"

class ProductSpecificationCreate(ProductSpecificationBase):
    pass

class ProductSpecificationResponse(ProductSpecificationBase):
    id: uuid.UUID
    product_version_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ChemicalComplianceSpecBase(BaseModel):
    chromium_vi_ppm: float = 0.0
    azo_dyes_ppm: float = 0.0
    formaldehyde_ppm: float = 12.0
    pfas_free: bool = True
    reach_svhc_status: str = "compliant"
    lab_test_report_id: Optional[str] = "TR-TUV-2026-8812"
    accredited_lab: str = "TÜV Rheinland / Eurofins"
    test_date: date = Field(default_factory=date.today)

class ChemicalComplianceSpecCreate(ChemicalComplianceSpecBase):
    pass

class ChemicalComplianceSpecResponse(ChemicalComplianceSpecBase):
    id: uuid.UUID
    product_version_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class TraceabilitySpecBase(BaseModel):
    abattoir_license_no: str = "APEDA-TN-7821"
    mandal_district: str = "Ambur / Tirupattur District"
    state: str = "Tamil Nadu"
    geolocation_lat: float = 12.7904
    geolocation_lng: float = 78.7163
    eudr_cutoff_cleared: bool = True
    hide_origin_batch: str = "BATCH-2026-TN-04"

class TraceabilitySpecCreate(TraceabilitySpecBase):
    pass

class TraceabilitySpecResponse(TraceabilitySpecBase):
    id: uuid.UUID
    product_version_id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

class ProductPassportResponse(BaseModel):
    id: uuid.UUID
    product_version_id: uuid.UUID
    passport_number: str
    public_token: str
    qr_code_url: Optional[str] = None
    carbon_footprint_kg_co2e: float = 4.2
    status: str
    recipient_buyer_id: Optional[uuid.UUID]
    generated_at: datetime
    passport_metadata: Dict[str, Any]
    model_config = ConfigDict(from_attributes=True)

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
    specifications: Optional[ProductSpecificationCreate] = None
    chemical_spec: Optional[ChemicalComplianceSpecCreate] = None
    traceability_spec: Optional[TraceabilitySpecCreate] = None

class ProductVersionResponse(ProductVersionBase):
    id: uuid.UUID
    product_family_id: uuid.UUID
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    created_at: datetime
    specifications: Optional[ProductSpecificationResponse] = None
    chemical_spec: Optional[ChemicalComplianceSpecResponse] = None
    traceability_spec: Optional[TraceabilitySpecResponse] = None
    certificates: List[ProductCertificateResponse] = Field(default_factory=list)
    passports: List[ProductPassportResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

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
    specifications: Optional[ProductSpecificationCreate] = None
    chemical_spec: Optional[ChemicalComplianceSpecCreate] = None
    traceability_spec: Optional[TraceabilitySpecCreate] = None

class ProductFamilyResponse(ProductFamilyBase):
    id: uuid.UUID
    tenant_id: Optional[uuid.UUID]
    created_at: datetime
    versions: List[ProductVersionResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
