import uuid
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.provenance import TruthStatus, SourceTier, SourceRegistry, EvidenceAssertion
from app.models.verification import VerificationQueue
from app.models.company import EntityCompany, EntityPerson
from app.repositories import verification_repo

STALE_THRESHOLD_DAYS = 90

def calculate_freshness(checked_at: Optional[datetime]) -> Tuple[bool, int, str]:
    """
    Calculate data freshness against 90-day SLA.
    Returns: (is_stale, days_old, freshness_label)
    """
    if not checked_at:
        return True, 999, "Unknown freshness (>90d)"
    
    # Ensure timezone aware comparison
    now = datetime.now(timezone.utc)
    if checked_at.tzinfo is None:
        checked_at = checked_at.replace(tzinfo=timezone.utc)

    delta = now - checked_at
    days_old = max(0, delta.days)
    is_stale = days_old > STALE_THRESHOLD_DAYS

    if is_stale:
        label = f"Stale ({days_old} days old - Re-verification recommended)"
    else:
        label = f"Fresh ({days_old} days old)"

    return is_stale, days_old, label

def resolve_effective_truth_status(
    base_status: TruthStatus,
    checked_at: Optional[datetime],
    source_tier: Optional[SourceTier] = None
) -> Tuple[TruthStatus, bool, str]:
    """
    Compute effective truth status accounting for stale data thresholds (>90d) and source reliability.
    """
    is_stale, days_old, label = calculate_freshness(checked_at)

    if base_status == TruthStatus.demo:
        return TruthStatus.demo, False, "Sample Record (Demo Environment)"
    
    if is_stale:
        return TruthStatus.stale, True, label

    return base_status, False, label

def execute_analyst_review(
    db: Session,
    queue_id: uuid.UUID,
    decision: str, # "approve", "reject", "dispute"
    notes: Optional[str] = None,
    evidence_reference: Optional[str] = None,
    reviewer: str = "Trade OS Senior Research Analyst"
) -> VerificationQueue:
    """
    Process analyst review for a queued entity claim and record audit trail.
    """
    item = db.execute(select(VerificationQueue).where(VerificationQueue.id == queue_id)).scalar_one_or_none()
    if not item:
        raise ValueError("Verification queue item not found.")

    if decision == "approve":
        item.status = "verified"
        new_truth = "verified"
    elif decision == "reject":
        item.status = "rejected"
        new_truth = "declared"
    elif decision == "dispute":
        item.status = "disputed"
        new_truth = "disputed"
    else:
        raise ValueError(f"Invalid review decision '{decision}'. Must be 'approve', 'reject', or 'dispute'.")

    item.completed_at = datetime.now(timezone.utc)
    item.assigned_to = reviewer
    item.notes = notes or f"Analyst review decision: {decision}"
    if evidence_reference:
        item.evidence_summary = f"{item.evidence_summary or ''} [Evidence: {evidence_reference}]".strip()

    # Update associated Entity Company or Person
    if item.entity_type == "company":
        comp = db.execute(select(EntityCompany).where(EntityCompany.id == item.entity_id)).scalar_one_or_none()
        if comp:
            comp.truth_status = new_truth
            comp.verified_by = reviewer
            comp.checked_at = datetime.now(timezone.utc)
    elif item.entity_type == "person":
        person = db.execute(select(EntityPerson).where(EntityPerson.id == item.entity_id)).scalar_one_or_none()
        if person:
            person.verification_status = new_truth

    db.commit()
    db.refresh(item)
    return item
