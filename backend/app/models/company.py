from datetime import datetime
import uuid
from typing import List, Optional
from sqlalchemy import String, Integer, Numeric, Boolean, Text, DateTime, ForeignKey, CHAR, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class EntityCompany(Base):
    __tablename__ = "entity_company"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    canonical_name: Mapped[str] = mapped_column(Text, nullable=False)
    legal_name: Mapped[Optional[str]] = mapped_column(Text)
    legal_entity_type: Mapped[Optional[str]] = mapped_column(Text, default="GmbH") # GmbH, AG, SARL, KG
    vat_number: Mapped[Optional[str]] = mapped_column(Text)
    lei: Mapped[Optional[str]] = mapped_column(Text)
    company_registry_id: Mapped[Optional[str]] = mapped_column(Text)
    registry_country: Mapped[Optional[str]] = mapped_column(CHAR(2), default="DE")
    domain: Mapped[Optional[str]] = mapped_column(Text)
    country_code: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    city: Mapped[Optional[str]] = mapped_column(Text)
    region: Mapped[Optional[str]] = mapped_column(Text)
    postal_code: Mapped[Optional[str]] = mapped_column(Text)
    website: Mapped[Optional[str]] = mapped_column(Text)
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text)
    segment: Mapped[str] = mapped_column(Text, default="Leather goods")
    description: Mapped[Optional[str]] = mapped_column(Text)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer)
    employee_range: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="active")
    confidence: Mapped[float] = mapped_column(Numeric, default=1.0)
    
    # Provenance & Verification
    truth_status: Mapped[str] = mapped_column(Text, default="demo")
    source_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now())
    verified_by: Mapped[Optional[str]] = mapped_column(Text, default="Trade OS Analyst")
    
    # Entity Resolution & Hierarchy
    entity_resolution_status: Mapped[str] = mapped_column(Text, default="linked") # unresolved, linked, merged, disputed
    parent_entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=True)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    persons: Mapped[List["EntityPerson"]] = relationship("EntityPerson", back_populates="company", cascade="all, delete-orphan")
    products: Mapped[List["EntityProduct"]] = relationship("EntityProduct", back_populates="company", cascade="all, delete-orphan")
    certifications: Mapped[List["EntityCertification"]] = relationship("EntityCertification", back_populates="company", cascade="all, delete-orphan")
    signals: Mapped[List["Signal"]] = relationship("Signal", back_populates="company", cascade="all, delete-orphan")
    match_candidate: Mapped[Optional["MatchCandidate"]] = relationship("MatchCandidate", back_populates="company", uselist=False)

class EntityPerson(Base):
    __tablename__ = "entity_person"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(Text)
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence: Mapped[float] = mapped_column(Numeric, default=0.8)
    verification_status: Mapped[str] = mapped_column(Text, default="demo")
    
    # Verification & GDPR Provenance
    confidence_rubric: Mapped[Optional[str]] = mapped_column(Text, default="Corporate website procurement imprint + sample dossier")
    contact_basis: Mapped[str] = mapped_column(Text, default="company_route") # verified_direct, company_route, inferred, unavailable
    lawful_source: Mapped[Optional[str]] = mapped_column(Text, default="German Trade Registry & Public Procurement Directory")
    correction_history: Mapped[dict] = mapped_column(JSONB, default=list)

    consent_status: Mapped[str] = mapped_column(Text, default="legitimate_interest")
    legal_basis: Mapped[str] = mapped_column(Text, default="B2B legitimate interest under GDPR Art. 6(1)(f)")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="persons")

class EntityProduct(Base):
    __tablename__ = "entity_product"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    hs_code: Mapped[Optional[str]] = mapped_column(Text)
    material_types: Mapped[dict] = mapped_column(JSONB, default=list)
    tannage: Mapped[dict] = mapped_column(JSONB, default=list)
    thickness_range_mm: Mapped[dict] = mapped_column(JSONB, default=list)
    finish: Mapped[dict] = mapped_column(JSONB, default=list)
    spec: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="products")
