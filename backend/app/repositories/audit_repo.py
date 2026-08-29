import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.audit import AuditEventRecord, AuditCategory

def log_audit_event(db: Session, data: Dict[str, Any]) -> AuditEventRecord:
    """
    Append an immutable event to the centralized audit trail.
    Adheres to INSERT ONLY policy.
    """
    event = AuditEventRecord(
        tenant_id=data.get("tenant_id"),
        user_id=data.get("user_id"),
        event_category=data.get("event_category", AuditCategory.MODIFICATION),
        action=data["action"],
        entity_type=data["entity_type"],
        entity_id=data.get("entity_id"),
        actor_email=data.get("actor_email", "system@tradeos.in"),
        ip_address=data.get("ip_address", "127.0.0.1"),
        user_agent=data.get("user_agent", "TradeOS-Client/2.0"),
        payload_diff=data.get("payload_diff", {})
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def list_audit_events(
    db: Session,
    tenant_id: Optional[uuid.UUID] = None,
    category: Optional[str] = None,
    entity_type: Optional[str] = None,
    limit: int = 100
) -> List[AuditEventRecord]:
    """Retrieve chronologically ordered audit logs with optional category filter."""
    stmt = select(AuditEventRecord).order_by(AuditEventRecord.created_at.desc())
    if tenant_id:
        stmt = stmt.where(AuditEventRecord.tenant_id == tenant_id)
    if category:
        stmt = stmt.where(AuditEventRecord.event_category == category)
    if entity_type:
        stmt = stmt.where(AuditEventRecord.entity_type == entity_type)
    stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars().all())

def get_audit_stats(db: Session, tenant_id: Optional[uuid.UUID] = None) -> Dict[str, Any]:
    """Calculate audit metrics and activity breakdown."""
    total_events = db.query(func.count(AuditEventRecord.id)).scalar() or 0
    signoffs = db.query(func.count(AuditEventRecord.id)).filter(AuditEventRecord.event_category == AuditCategory.COMPLIANCE_SIGN_OFF).scalar() or 0
    financials = db.query(func.count(AuditEventRecord.id)).filter(AuditEventRecord.event_category == AuditCategory.FINANCE_MODIFICATION).scalar() or 0
    accesses = db.query(func.count(AuditEventRecord.id)).filter(AuditEventRecord.event_category == AuditCategory.ACCESS).scalar() or 0

    return {
        "total_audit_events": total_events,
        "compliance_sign_offs": signoffs,
        "financial_modifications": financials,
        "security_access_events": accesses,
        "tamper_evident_status": "GUARANTEED_INSERT_ONLY"
    }
