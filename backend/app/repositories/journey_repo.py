import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.journey import StageEvent

def insert_stage_event(
    db: Session,
    entity_type: str,
    entity_id: uuid.UUID,
    macro_stage: str,
    previous_stage: str,
    new_stage: str,
    action: str,
    actor: str,
    actor_role: str = "owner",
    reason_code: str = "workflow_progression",
    notes: Optional[str] = None,
    evidence_references: Optional[Dict[str, Any]] = None,
    idempotency_key: Optional[str] = None,
    tenant_id: Optional[uuid.UUID] = None
) -> StageEvent:
    """
    Insert an immutable stage transition event.
    Never update or delete existing stage events.
    """
    event = StageEvent(
        tenant_id=tenant_id,
        entity_type=entity_type,
        entity_id=entity_id,
        macro_stage=macro_stage,
        previous_stage=previous_stage,
        new_stage=new_stage,
        action=action,
        actor=actor,
        actor_role=actor_role,
        reason_code=reason_code,
        notes=notes,
        evidence_references=evidence_references or {},
        idempotency_key=idempotency_key
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_event_by_idempotency_key(db: Session, idempotency_key: str) -> Optional[StageEvent]:
    """Check for existing event with the given idempotency key."""
    stmt = select(StageEvent).where(StageEvent.idempotency_key == idempotency_key)
    return db.execute(stmt).scalar_one_or_none()

def list_stage_events_for_entity(
    db: Session,
    entity_type: str,
    entity_id: uuid.UUID
) -> List[StageEvent]:
    """Retrieve immutable chronological event history for an entity."""
    stmt = (
        select(StageEvent)
        .where(
            and_(
                StageEvent.entity_type == entity_type,
                StageEvent.entity_id == entity_id
            )
        )
        .order_by(StageEvent.created_at.asc())
    )
    return list(db.execute(stmt).scalars().all())
