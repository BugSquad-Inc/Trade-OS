from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ActivationKPISchema(BaseModel):
    profile_completeness_pct: float
    dossier_completeness_pct: float
    match_explainability_pct: float
    verified_contacts_count: int

class GTMKPISchema(BaseModel):
    total_buyers_monitored: int
    grade_a_matches: int
    grade_b_matches: int
    active_signals_count: int
    total_customs_teu: float
    enterprise_mrr_pipeline_usd: float

class ExecutiveKPIDashboardResponse(BaseModel):
    timestamp: str
    active_exporter: str
    exporter_origin: str
    activation: ActivationKPISchema
    gtm: GTMKPISchema
    recent_agent_runs: int
    crm_exports_count: int
