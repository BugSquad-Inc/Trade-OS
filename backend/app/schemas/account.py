from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ContactDetail(BaseModel):
    id: str
    full_name: str
    title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_primary: bool
    confidence: float
    verification_status: str
    consent_status: str
    legal_basis: str

class ProductDetail(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    hs_code: Optional[str] = None
    material_types: List[str]
    tannage: List[str]
    thickness_range_mm: List[str]
    finish: List[str]

class CertificationDetail(BaseModel):
    id: str
    certification_type: str
    certification_name: str
    issued_by: Optional[str] = None
    status: str
    valid_until: Optional[str] = None

class Account360Response(BaseModel):
    id: str
    canonical_name: str
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    country_code: str
    country: str
    city: Optional[str] = None
    region: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    segment: str
    description: Optional[str] = None
    founded_year: Optional[int] = None
    employee_range: Optional[str] = None
    status: str
    match_score: Optional[float] = None
    grade: Optional[str] = None
    rank: Optional[int] = None
    drivers: List[Dict[str, Any]] = []
    key_gaps: List[str] = []
    next_best_action: Optional[str] = None
    outreach_angle: Optional[str] = None
    contacts: List[ContactDetail] = []
    products: List[ProductDetail] = []
    certifications: List[CertificationDetail] = []
    signals: List[Dict[str, Any]] = []
    eudr_requirements: List[Dict[str, Any]] = []
    lane_economics: Dict[str, Any] = {}
