from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class HybridSearchRequest(BaseModel):
    query: str
    target_country: Optional[str] = None
    target_segment: Optional[str] = None
    top_k: int = 10
    dense_weight: float = 0.5
    sparse_weight: float = 0.5

class SearchResultItem(BaseModel):
    company_id: str
    canonical_name: str
    country_code: str
    city: Optional[str] = None
    segment: str
    description: Optional[str] = None
    dense_rank: Optional[int] = None
    sparse_rank: Optional[int] = None
    rrf_score: float
    relevance_explanation: str
    match_score: Optional[float] = None
    grade: Optional[str] = None

class HybridSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResultItem]
    execution_time_ms: float
