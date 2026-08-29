import uuid
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.deal import OpportunityStage

class TaskItemResponse(BaseModel):
    id: uuid.UUID
    opportunity_id: Optional[uuid.UUID] = None
    buyer_id: Optional[uuid.UUID] = None
    title: str
    description: Optional[str] = None
    due_date: date
    priority: str
    status: str
    task_type: str
    assigned_to: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

class QuoteResponse(BaseModel):
    id: uuid.UUID
    opportunity_id: uuid.UUID
    quote_number: str
    product_version_id: Optional[uuid.UUID] = None
    quantity_sqft: int
    unit_price_inr: float
    unit_price_eur: float
    fx_rate_eur_inr: float
    estimated_freight_usd: float
    customs_duty_pct: float
    insurance_usd: float
    landed_cost_eur_per_sqft: float
    gross_margin_pct: float
    total_quote_value_eur: float
    payment_terms: str
    lead_time_days: int
    status: str
    valid_until: date
    created_at: datetime

    model_config = {"from_attributes": True}

class OpportunityBase(BaseModel):
    buyer_id: uuid.UUID
    product_family_id: Optional[uuid.UUID] = None
    product_version_id: Optional[uuid.UUID] = None
    title: str
    stage: OpportunityStage = OpportunityStage.matched
    deal_value_eur: float = 0.0
    deal_value_inr: float = 0.0
    volume_sqft: int = 5000
    incoterms: str = "CIF Hamburg"
    target_close_date: Optional[date] = None
    probability: float = 0.3
    owner: str = "Sales Lead"
    notes: Optional[str] = None

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdateStage(BaseModel):
    stage: OpportunityStage
    notes: Optional[str] = None

class OpportunityResponse(OpportunityBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    quotes: List[QuoteResponse] = Field(default_factory=list)
    tasks: List[TaskItemResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}

class QuoteCreateRequest(BaseModel):
    product_version_id: Optional[uuid.UUID] = None
    freight_lane_id: Optional[uuid.UUID] = None
    unit_price_inr: float = 295.0
    quantity_sqft: int = 5000
    freight_usd: float = 1850.0
    insurance_usd: float = 120.0
    customs_duty_pct: float = 0.0
    target_margin_pct: float = 25.0
    fx_rate_eur_inr: float = 92.5
    payment_terms: Optional[str] = "30% Advance, 70% against B/L"
    lead_time_days: int = 30
    valid_until: Optional[date] = None

class LandedCostCalculatorRequest(BaseModel):
    unit_price_inr: float
    quantity_sqft: int = 5000
    freight_usd: float = 1850.0
    insurance_usd: float = 120.0
    customs_duty_pct: float = 0.0
    target_margin_pct: float = 25.0
    fx_rate_eur_inr: float = 92.5

class LandedCostCalculatorResponse(BaseModel):
    unit_price_inr: float
    fx_rate_eur_inr: float
    base_eur_per_sqft: float
    freight_eur_per_sqft: float
    insurance_eur_per_sqft: float
    duty_eur_per_sqft: float
    landed_cost_eur_per_sqft: float
    recommended_unit_price_eur: float
    total_quote_value_eur: float
    total_quote_value_inr: float
    gross_margin_pct: float
    quantity_sqft: int

class PipelineSummaryResponse(BaseModel):
    total_active_deals: int
    total_pipeline_eur: float
    total_won_eur: float
    stage_counts: Dict[str, int]

class TodayCockpitResponse(BaseModel):
    date: str
    exporter_name: str
    readiness_score: int
    urgent_tasks: List[TaskItemResponse]
    pipeline_summary: PipelineSummaryResponse
    recommended_actions: List[Dict[str, Any]]
