from pydantic import BaseModel
from typing import List, Optional
import uuid

class ExporterCapabilityResponse(BaseModel):
    id: str
    company_name: str
    location: str
    cluster: str
    export_market_focus: List[str]
    material_types: List[str]
    tannage: List[str]
    thickness_range_mm: List[str]
    finish_capabilities: List[str]
    monthly_capacity_sqft: int
    moq_sqft: int
    lead_time_days: int
    sample_lead_time_days: int
    port_of_export: str
    incoterms: List[str]
    certifications: List[str]
    eudr_readiness_score: int
    eudr_gap_summary: Optional[str] = None
