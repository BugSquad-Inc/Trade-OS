import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

class VerificationQueue(Base):
    __tablename__ = "verification_queue"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False) # company, person, signal, customs
    entity_name: Mapped[str] = mapped_column(String(255), nullable=False)
    claim_type: Mapped[str] = mapped_column(String(100), default="buyer_procurement_intent")
    priority: Mapped[str] = mapped_column(String(20), default="medium") # high, medium, low
    status: Mapped[str] = mapped_column(String(50), default="pending") # pending, in_review, verified, rejected
    assigned_to: Mapped[Optional[str]] = mapped_column(String(100), default="Trade OS Senior Research Analyst")
    evidence_summary: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

class EntityResolutionLink(Base):
    __tablename__ = "entity_resolution_link"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=False)
    target_entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=False)
    link_type: Mapped[str] = mapped_column(String(50), default="brand_subsidiary") # subsidiary, brand_subsidiary, duplicate, trade_alias
    confidence: Mapped[float] = mapped_column(Float, default=0.95)
    evidence: Mapped[dict] = mapped_column(JSONB, default=lambda: {"source": "German Commercial Register (Handelsregister)"})
    reviewer: Mapped[Optional[str]] = mapped_column(String(100), default="Entity Resolution Engine")
    status: Mapped[str] = mapped_column(String(50), default="confirmed")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class CorrectionRecord(Base):
    __tablename__ = "correction_record"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False) # company, person, signal
    field_name: Mapped[str] = mapped_column(String(100), nullable=False)
    old_value: Mapped[Optional[str]] = mapped_column(Text)
    new_value: Mapped[str] = mapped_column(Text, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    reporter_email: Mapped[str] = mapped_column(String(255), default="exporter_user@butlers.in")
    status: Mapped[str] = mapped_column(String(50), default="submitted") # submitted, applied, rejected
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
