import uuid
from enum import Enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base

class TruthStatus(str, Enum):
    verified = "verified"
    inferred = "inferred"
    customer_supplied = "customer_supplied"
    provider_supplied = "provider_supplied"
    demo = "demo"
    stale = "stale"
    disputed = "disputed"
    unavailable = "unavailable"

class SourceTier(str, Enum):
    tier_a = "tier_a"  # Authoritative (Government portals, official registries)
    tier_b = "tier_b"  # Licensed commercial databases
    tier_c = "tier_c"  # Public web / trade directories
    tier_d = "tier_d"  # Inferred by models / analysts
    tier_e = "tier_e"  # Demo / synthetic test data

class SourceRegistry(Base):
    __tablename__ = "source_registry"
    __table_args__ = {"schema": "gold"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    source_tier = Column(SQLEnum(SourceTier, name="source_tier_enum", schema="gold"), default=SourceTier.tier_e, nullable=False)
    licence_terms = Column(Text, nullable=True)
    usage_policy = Column(String(255), nullable=True)
    owner = Column(String(100), default="Trade OS Data Operations")
    is_active = Column(Boolean, default=True, nullable=False)
    checked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    evidence_assertions = relationship("EvidenceAssertion", back_populates="source", cascade="all, delete-orphan")

class EvidenceAssertion(Base):
    __tablename__ = "evidence_assertion"
    __table_args__ = {"schema": "gold"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_type = Column(String(100), nullable=False, index=True)  # e.g., "buyer_interest", "certification", "contact_role", "freight_quote"
    claim_value = Column(JSONB, nullable=False)
    truth_status = Column(SQLEnum(TruthStatus, name="truth_status_enum", schema="gold"), default=TruthStatus.demo, nullable=False, index=True)
    source_id = Column(UUID(as_uuid=True), ForeignKey("gold.source_registry.id"), nullable=True)
    confidence = Column(Float, default=1.0, nullable=False)
    verification_method = Column(String(255), nullable=True)
    reviewed_by = Column(String(100), nullable=True)
    tenant_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    metadata_info = Column("metadata", JSONB, default=dict)
    valid_from = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=True)
    checked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    source = relationship("SourceRegistry", back_populates="evidence_assertions")
