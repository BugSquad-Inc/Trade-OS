import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func
from app.models.deal import Opportunity, OpportunityStage, Quote, TaskItem
from app.models.company import EntityCompany
from app.models.product import ProductFamily, ProductVersion
from app.services.quote_service import calculate_landed_cost

def list_opportunities(db: Session, stage_filter: Optional[str] = None) -> List[Opportunity]:
    """List opportunities with buyer and product details."""
    stmt = (
        select(Opportunity)
        .options(
            joinedload(Opportunity.buyer),
            joinedload(Opportunity.product_family),
            joinedload(Opportunity.quotes)
        )
        .order_by(Opportunity.created_at.desc())
    )
    if stage_filter:
        stmt = stmt.where(Opportunity.stage == stage_filter)
    return list(db.execute(stmt).unique().scalars().all())

def get_opportunity(db: Session, opp_id: uuid.UUID) -> Optional[Opportunity]:
    """Get single opportunity by ID."""
    stmt = (
        select(Opportunity)
        .options(
            joinedload(Opportunity.buyer),
            joinedload(Opportunity.product_family),
            joinedload(Opportunity.product_version),
            joinedload(Opportunity.quotes),
            joinedload(Opportunity.tasks)
        )
        .where(Opportunity.id == opp_id)
    )
    return db.execute(stmt).unique().scalar_one_or_none()

def create_opportunity(db: Session, data: Dict[str, Any]) -> Opportunity:
    """Create a new buyer deal opportunity."""
    stage = data.get("stage", OpportunityStage.matched)
    opp = Opportunity(
        buyer_id=data["buyer_id"],
        product_family_id=data.get("product_family_id"),
        product_version_id=data.get("product_version_id"),
        title=data["title"],
        stage=stage,
        deal_value_eur=data.get("deal_value_eur", 0.0),
        deal_value_inr=data.get("deal_value_inr", 0.0),
        volume_sqft=data.get("volume_sqft", 5000),
        incoterms=data.get("incoterms", "CIF Hamburg"),
        target_close_date=data.get("target_close_date"),
        probability=data.get("probability", 0.3),
        owner=data.get("owner", "Sales Lead"),
        notes=data.get("notes")
    )
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return get_opportunity(db, opp.id)

def update_opportunity_stage(db: Session, opp_id: uuid.UUID, stage: OpportunityStage, notes: Optional[str] = None) -> Optional[Opportunity]:
    """Move deal to a new stage in the 12-stage lifecycle."""
    opp = get_opportunity(db, opp_id)
    if not opp:
        return None
    opp.stage = stage
    if notes:
        opp.notes = f"{opp.notes}\n[{datetime.now().strftime('%Y-%m-%d')}] {notes}" if opp.notes else notes
    db.commit()
    db.refresh(opp)
    return opp

def create_quote(db: Session, opp_id: uuid.UUID, data: Dict[str, Any]) -> Quote:
    """Calculate landed cost and create quotation for an opportunity."""
    calc = calculate_landed_cost(
        unit_price_inr=data.get("unit_price_inr", 295.0),
        quantity_sqft=data.get("quantity_sqft", 5000),
        freight_usd=data.get("freight_usd", 1850.0),
        insurance_usd=data.get("insurance_usd", 120.0),
        customs_duty_pct=data.get("customs_duty_pct", 0.0),
        target_margin_pct=data.get("target_margin_pct", 25.0),
        fx_rate_eur_inr=data.get("fx_rate_eur_inr", 92.5)
    )

    quote = Quote(
        opportunity_id=opp_id,
        product_version_id=data.get("product_version_id"),
        freight_lane_id=data.get("freight_lane_id"),
        quantity_sqft=calc["quantity_sqft"],
        unit_price_inr=calc["unit_price_inr"],
        unit_price_eur=calc["recommended_unit_price_eur"],
        fx_rate_eur_inr=calc["fx_rate_eur_inr"],
        estimated_freight_usd=data.get("freight_usd", 1850.0),
        customs_duty_pct=data.get("customs_duty_pct", 0.0),
        insurance_usd=data.get("insurance_usd", 120.0),
        landed_cost_eur_per_sqft=calc["landed_cost_eur_per_sqft"],
        gross_margin_pct=calc["gross_margin_pct"],
        total_quote_value_eur=calc["total_quote_value_eur"],
        payment_terms=data.get("payment_terms", "30% Advance, 70% against B/L"),
        lead_time_days=data.get("lead_time_days", 30),
        status="sent",
        valid_until=data.get("valid_until", date.today())
    )
    db.add(quote)

    # Also update Opportunity deal value
    opp = db.execute(select(Opportunity).where(Opportunity.id == opp_id)).scalar_one_or_none()
    if opp:
        opp.deal_value_eur = calc["total_quote_value_eur"]
        opp.deal_value_inr = calc["total_quote_value_inr"]
        opp.volume_sqft = calc["quantity_sqft"]
        opp.stage = OpportunityStage.quote_sent

    db.commit()
    db.refresh(quote)
    return quote

def list_today_tasks(db: Session, status_filter: Optional[str] = "todo") -> List[TaskItem]:
    """Retrieve actionable tasks for the Today morning cockpit."""
    stmt = (
        select(TaskItem)
        .options(joinedload(TaskItem.buyer), joinedload(TaskItem.opportunity))
        .order_by(TaskItem.due_date.asc())
    )
    if status_filter:
        stmt = stmt.where(TaskItem.status == status_filter)
    return list(db.execute(stmt).scalars().all())

def complete_task(db: Session, task_id: uuid.UUID) -> Optional[TaskItem]:
    """Mark a task as completed."""
    stmt = select(TaskItem).where(TaskItem.id == task_id)
    task = db.execute(stmt).scalar_one_or_none()
    if task:
        task.status = "completed"
        task.completed_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(task)
    return task

def get_pipeline_summary(db: Session) -> Dict[str, Any]:
    """Get active pipeline totals and counts by stage."""
    opps = db.execute(select(Opportunity)).scalars().all()
    
    total_pipeline_eur = sum(o.deal_value_eur for o in opps if o.stage not in (OpportunityStage.closed_lost, OpportunityStage.closed_won))
    total_won_eur = sum(o.deal_value_eur for o in opps if o.stage == OpportunityStage.closed_won)
    total_active_deals = sum(1 for o in opps if o.stage not in (OpportunityStage.closed_lost, OpportunityStage.closed_won))
    
    stage_counts = {}
    for s in OpportunityStage:
        stage_counts[s.value] = sum(1 for o in opps if o.stage == s)

    return {
        "total_active_deals": total_active_deals,
        "total_pipeline_eur": round(total_pipeline_eur, 2),
        "total_won_eur": round(total_won_eur, 2),
        "stage_counts": stage_counts
    }
