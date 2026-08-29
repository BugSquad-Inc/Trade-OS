import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.audit import AuditEventCreate, AuditEventResponse, AuditStatsResponse
from app.repositories import audit_repo

router = APIRouter(prefix="/api/v1/audit", tags=["Centralized Compliance & Security Audit"], dependencies=[Depends(require_api_key)])

@router.get("/events", response_model=List[AuditEventResponse])
def get_audit_trail(
    category: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Retrieve immutable audit event trail."""
    return audit_repo.list_audit_events(db, category=category, entity_type=entity_type, limit=limit)

@router.post("/events", response_model=AuditEventResponse)
def log_audit_event_entry(event_in: AuditEventCreate, db: Session = Depends(get_db)):
    """Log an immutable audit trail entry."""
    return audit_repo.log_audit_event(db, event_in.model_dump())

@router.get("/stats", response_model=AuditStatsResponse)
def get_audit_trail_statistics(db: Session = Depends(get_db)):
    """Get audit trail health, compliance sign-offs count, and tamper-evident guarantees."""
    return audit_repo.get_audit_stats(db)
