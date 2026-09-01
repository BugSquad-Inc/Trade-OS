import uuid
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, Text, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

class TruthStatus(str, Enum):
    verified = "verified"
    declared = "declared"
    customer_supplied = "customer_supplied"
    estimated = "estimated"
    inferred = "inferred"
    checked = "checked"
    demo = "demo"
    stale = "stale"
    needs_professional_confirmation = "needs_professional_confirmation"
    disputed = "disputed"
    provider_supplied = "provider_supplied"
    unavailable = "unavailable"

class SourceTier(str, Enum):
    tier_a = "tier_a"  # Authoritative (DGFT, ICEGATE, German Handelsregister, APEDA)
    tier_b = "tier_b"  # Licensed commercial databases (Panjiva, D&B, SGS)
    tier_c = "tier_c"  # Public web / trade directories (Wer Liefert Was, CLE)
    tier_d = "tier_d"  # Inferred by models / heuristic scoring
    tier_e = "tier_e"  # Demo / synthetic test data

class SourceRegistry(Base):
    __tablename__ = "source_registry"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    source_tier: Mapped[SourceTier] = mapped_column(
        SQLEnum(SourceTier, name="source_tier_enum", schema="gold", values_callable=lambda obj: [e.value for e in obj]),
        default=SourceTier.tier_e,
        nullable=False
    )
    licence_terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    usage_policy: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    owner: Mapped[str] = mapped_column(String(100), default="Trade OS Data Operations")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    evidence_assertions = relationship("EvidenceAssertion", back_populates="source", cascade="all, delete-orphan")

class EvidenceAssertion(Base):
    __tablename__ = "evidence_assertion"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # buyer_procurement_intent, certification, contact_role, freight_quote
    claim_value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    truth_status: Mapped[TruthStatus] = mapped_column(
        SQLEnum(TruthStatus, name="truth_status_enum", schema="gold", values_callable=lambda obj: [e.value for e in obj]),
        default=TruthStatus.demo,
        nullable=False,
        index=True
    )
    source_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.source_registry.id"), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    verification_method: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reviewed_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    metadata_info: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    source = relationship("SourceRegistry", back_populates="evidence_assertions")
