import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.deal import (
    OpportunityCreate,
    OpportunityResponse,
    OpportunityUpdateStage,
    QuoteCreateRequest,
    QuoteResponse,
    LandedCostCalculatorRequest,
    LandedCostCalculatorResponse,
    PipelineSummaryResponse
)
from app.repositories import deal_repo
from app.services.quote_service import calculate_landed_cost

router = APIRouter(prefix="/api/v1/deals", tags=["Deals, Quotes & Pipeline"], dependencies=[Depends(require_api_key)])

@router.get("", response_model=List[OpportunityResponse])
def list_deals(stage: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """List opportunities in the 12-stage export pipeline."""
    return deal_repo.list_opportunities(db, stage_filter=stage)

@router.post("", response_model=OpportunityResponse)
def create_deal(deal_in: OpportunityCreate, db: Session = Depends(get_db)):
    """Create a new buyer export deal opportunity."""
    return deal_repo.create_opportunity(db, deal_in.model_dump())

@router.get("/summary/pipeline", response_model=PipelineSummaryResponse)
def get_pipeline_summary(db: Session = Depends(get_db)):
    """Get active pipeline totals, win metrics, and stage counts."""
    return deal_repo.get_pipeline_summary(db)

@router.post("/calculator/landed-cost", response_model=LandedCostCalculatorResponse)
def compute_landed_cost(req: LandedCostCalculatorRequest):
    """Compute FOB INR to European Landed Cost in EUR with ocean freight, duty, and target gross margin."""
    return calculate_landed_cost(
        unit_price_inr=req.unit_price_inr,
        quantity_sqft=req.quantity_sqft,
        freight_usd=req.freight_usd,
        insurance_usd=req.insurance_usd,
        customs_duty_pct=req.customs_duty_pct,
        target_margin_pct=req.target_margin_pct,
        fx_rate_eur_inr=req.fx_rate_eur_inr
    )

@router.get("/{opp_id}", response_model=OpportunityResponse)
def get_deal(opp_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve single opportunity with quotations and task history."""
    opp = deal_repo.get_opportunity(db, opp_id)
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal opportunity not found.")
    return opp

@router.patch("/{opp_id}/stage", response_model=OpportunityResponse)
def update_deal_stage(opp_id: uuid.UUID, stage_in: OpportunityUpdateStage, db: Session = Depends(get_db)):
    """Move deal along the 12-stage export lifecycle."""
    opp = deal_repo.update_opportunity_stage(db, opp_id, stage=stage_in.stage, notes=stage_in.notes)
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal opportunity not found.")
    return opp

@router.post("/{opp_id}/quotes", response_model=QuoteResponse)
def issue_quote(opp_id: uuid.UUID, quote_in: QuoteCreateRequest, db: Session = Depends(get_db)):
    """Generate and attach official Landed-Cost quotation for an export opportunity."""
    opp = deal_repo.get_opportunity(db, opp_id)
    if not opp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Deal opportunity not found.")
    return deal_repo.create_quote(db, opp_id, quote_in.model_dump())
