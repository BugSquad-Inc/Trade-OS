import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.verification import VerificationQueue, EntityResolutionLink, CorrectionRecord
from app.models.company import EntityCompany, EntityPerson

def list_verification_queue(db: Session, status_filter: Optional[str] = None) -> List[VerificationQueue]:
    """Retrieve analyst verification queue items."""
    stmt = select(VerificationQueue)
    if status_filter:
        stmt = stmt.where(VerificationQueue.status == status_filter)
    stmt = stmt.order_by(VerificationQueue.created_at.desc())
    return list(db.execute(stmt).scalars().all())

def sign_off_claim(db: Session, queue_id: uuid.UUID, approved: bool, notes: Optional[str] = None, reviewer: str = "Trade OS Senior Analyst") -> Optional[VerificationQueue]:
    """Approve or reject a claim in the verification queue."""
    item = db.execute(select(VerificationQueue).where(VerificationQueue.id == queue_id)).scalar_one_or_none()
    if not item:
        return None

    item.status = "verified" if approved else "rejected"
    item.completed_at = datetime.now(timezone.utc)
    if notes:
        item.notes = notes
    item.assigned_to = reviewer

    # If verifying a company or contact, update its status
    if approved:
        if item.entity_type == "company":
            comp = db.execute(select(EntityCompany).where(EntityCompany.id == item.entity_id)).scalar_one_or_none()
            if comp:
                comp.truth_status = "verified"
                comp.verified_by = reviewer
                comp.checked_at = datetime.now(timezone.utc)
        elif item.entity_type == "person":
            person = db.execute(select(EntityPerson).where(EntityPerson.id == item.entity_id)).scalar_one_or_none()
            if person:
                person.verification_status = "verified"

    db.commit()
    db.refresh(item)
    return item

def submit_correction(db: Session, data: Dict[str, Any]) -> CorrectionRecord:
    """Submit a customer or analyst data correction record."""
    correction = CorrectionRecord(
        entity_id=data["entity_id"],
        entity_type=data.get("entity_type", "company"),
        field_name=data["field_name"],
        old_value=data.get("old_value"),
        new_value=data["new_value"],
        reason=data["reason"],
        reporter_email=data.get("reporter_email", "exporter@butlers.in"),
        status="submitted"
    )
    db.add(correction)
    db.commit()
    db.refresh(correction)
    return correction

def list_entity_resolution_links(db: Session) -> List[EntityResolutionLink]:
    """List entity resolution links (brand-to-company parent mappings)."""
    stmt = select(EntityResolutionLink).order_by(EntityResolutionLink.created_at.desc())
    return list(db.execute(stmt).scalars().all())

def create_entity_resolution_link(db: Session, data: Dict[str, Any]) -> EntityResolutionLink:
    """Create or link brand/subsidiary to parent legal entity."""
    link = EntityResolutionLink(
        source_entity_id=data["source_entity_id"],
        target_entity_id=data["target_entity_id"],
        link_type=data.get("link_type", "brand_subsidiary"),
        confidence=data.get("confidence", 0.95),
        evidence=data.get("evidence", {"source": "Commercial registry mapping"}),
        reviewer=data.get("reviewer", "Trade OS Analyst")
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link
