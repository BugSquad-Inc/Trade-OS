from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class IngestionRunItem(BaseModel):
    id: str
    source_name: str
    status: str
    started_at: str
    finished_at: Optional[str] = None
    stats: Dict[str, Any] = {}
    error: Optional[str] = None

class IngestionStatusResponse(BaseModel):
    runs: List[IngestionRunItem]
    total_runs: int
    active_sources: int

class TriggerIngestionRequest(BaseModel):
    source_type: str = "trade_shows"  # trade_shows | regulatory | linkedin_signals
    batch_size: int = 50

class TriggerIngestionResponse(BaseModel):
    status: str
    message: str
    run_id: Optional[str] = None
    stats: Dict[str, Any] = {}

class PipelineRefreshResponse(BaseModel):
    status: str
    message: str
    buyers_scored: int
    signals_updated: int
    duration_ms: float
