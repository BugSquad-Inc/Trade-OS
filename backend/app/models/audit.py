import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

class AuditCategory(str, Enum):
    AUTH = "AUTH"
    ACCESS = "ACCESS"
    MODIFICATION = "MODIFICATION"
    EXPORT_DATA = "EXPORT_DATA"
    COMPLIANCE_SIGN_OFF = "COMPLIANCE_SIGN_OFF"
    FINANCE_MODIFICATION = "FINANCE_MODIFICATION"

class AuditEventRecord(Base):
    """
    Append-only centralized compliance and security audit log.
    In adherence to RULES.md Rule 8: audit.audit_event is INSERT ONLY. Never UPDATE or DELETE.
    """
    __tablename__ = "audit_event_record"
    __table_args__ = {"schema": "audit"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.tenant.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.user_account.id", ondelete="SET NULL"), nullable=True, index=True)
    
    event_category: Mapped[AuditCategory] = mapped_column(
        SQLEnum(AuditCategory, name="audit_category_enum", schema="audit"),
        default=AuditCategory.MODIFICATION,
        nullable=False,
        index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    
    actor_email: Mapped[str] = mapped_column(String(255), default="system@tradeos.in", nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), default="127.0.0.1")
    user_agent: Mapped[str] = mapped_column(String(255), default="TradeOS-Client/2.0")
    
    payload_diff: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
