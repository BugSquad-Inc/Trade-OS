from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DriverItem(BaseModel):
    category: str
    weight: int
    score: float
    title: str
    evidence: str

class ContactSummary(BaseModel):
    full_name: str
    title: Optional[str] = None
    email: Optional[str] = None
    confidence: float
    verification_status: str

class ScoreBreakdown(BaseModel):
    product_fit: float
    compliance: float
    lane_economics: float
    intent_signals: float
    accessibility: float

class MatchCardResponse(BaseModel):
    id: str
    buyer_id: str
    name: str
    legal_name: str
    country_code: str
    country: str
    city: str
    segment: str
    rank: int
    total_score: float
    grade: str
    score_breakdown: ScoreBreakdown
    drivers: List[Dict[str, Any]]
    key_gaps: List[str]
    next_best_action: str
    outreach_angle: str
    status: str
    contact: Optional[ContactSummary] = None
    freight_summary: str
    eudr_readiness_score: int

class MatchListResponse(BaseModel):
    matches: List[MatchCardResponse]
    total_count: int
    generated_at: str
