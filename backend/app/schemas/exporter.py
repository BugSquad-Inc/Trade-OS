import uuid
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ExporterProfileBase(BaseModel):
    company_name: str
    location: str
    cluster: str
    export_market_focus: List[str] = Field(default_factory=lambda: ["Germany", "EU"])
    material_types: List[str] = Field(default_factory=list)
    tannage: List[str] = Field(default_factory=list)
    thickness_range_mm: List[str] = Field(default_factory=list)
    finish_capabilities: List[str] = Field(default_factory=list)
    monthly_capacity_sqft: int = 50000
    moq_sqft: int = 3000
    lead_time_days: int = 35
    sample_lead_time_days: int = 10
    port_of_export: str = "Chennai Port (INMAA)"
    incoterms: List[str] = Field(default_factory=lambda: ["FOB", "CIF"])
    certifications: List[str] = Field(default_factory=list)
    eudr_readiness_score: int = 68
    eudr_gap_summary: Optional[str] = None

    # India-SMB Specific
    pan: Optional[str] = None
    gstin_list: List[str] = Field(default_factory=list)
    iec: Optional[str] = None
    udyam_number: Optional[str] = None
    rcmc_number: Optional[str] = None
    rcmc_expiry: Optional[date] = None
    lut_status: Optional[str] = "active"
    lut_expiry: Optional[date] = None
    ad_code: Optional[str] = None
    ad_bank_branch: Optional[str] = None
    ad_bank_ifsc: Optional[str] = None
    icegate_status: Optional[str] = "registered"
    authorised_signatory: Optional[str] = None
    facilities: List[Dict[str, Any]] = Field(default_factory=list)
    ports: List[str] = Field(default_factory=list)
    incoterms_preference: List[str] = Field(default_factory=list)
    commercial_constraints: Optional[str] = None

class ExporterProfileUpdate(BaseModel):
    company_name: Optional[str] = None
    location: Optional[str] = None
    cluster: Optional[str] = None
    pan: Optional[str] = None
    gstin_list: Optional[List[str]] = None
    iec: Optional[str] = None
    udyam_number: Optional[str] = None
    rcmc_number: Optional[str] = None
    rcmc_expiry: Optional[date] = None
    lut_status: Optional[str] = None
    ad_code: Optional[str] = None
    ad_bank_branch: Optional[str] = None
    monthly_capacity_sqft: Optional[int] = None
    moq_sqft: Optional[int] = None
    lead_time_days: Optional[int] = None

class ExporterOnboardingStepRequest(BaseModel):
    step: int = Field(..., ge=1, le=5, description="1: Company, 2: Registrations, 3: Facilities, 4: Products, 5: Review")
    data: Dict[str, Any]

class ExporterProfileResponse(ExporterProfileBase):
    id: uuid.UUID
    onboarding_step: int
    onboarding_status: str
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    evidence_status: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ReadinessGapResponse(BaseModel):
    status: str
    overall_score: int
    mandatory_checks: Dict[str, bool]
    recommended_checks: Dict[str, bool]
    missing_mandatory: List[str]
    missing_recommended: List[str]
    remediation_tasks: List[Dict[str, Any]]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
