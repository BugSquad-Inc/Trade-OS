from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SignalItem(BaseModel):
    id: str
    entity_id: str
    company_name: str
    category: str
    severity: str
    title: str
    summary: str
    quote: Optional[str] = None
    source_url: Optional[str] = None
    detected_at: str
    score: float
    evidence: Dict[str, Any]

class EUDRChecklistItem(BaseModel):
    item: str
    status: str
    article: str
    gap_detail: Optional[str] = None

class EUDRScorecardResponse(BaseModel):
    entity: str
    readiness_score: int
    status: str
    requirements: List[EUDRChecklistItem]
    top_gap: str
    recommended_action: str

class FreightBenchmarkResponse(BaseModel):
    origin_port: str
    destination_port: str
    mode: str
    container_type: str
    rate_usd: float
    rate_spread: str
    transit_days: str
    port_congestion_index: str
    reroute_risk_notes: Optional[str] = None
    sample_air_transit: str

class SignalListResponse(BaseModel):
    signals: List[SignalItem]
    total_count: int
    eudr_scorecard: EUDRScorecardResponse
    freight_benchmark: FreightBenchmarkResponse
