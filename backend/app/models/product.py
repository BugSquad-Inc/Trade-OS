import uuid
from datetime import datetime, date, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Boolean, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

class ProductFamily(Base):
    __tablename__ = "product_family"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), default="Finished Leather")
    hs_code: Mapped[str] = mapped_column(String(20), default="4107")
    itc_hs_code: Mapped[Optional[str]] = mapped_column(String(20), default="4107.12.00")
    leather_type: Mapped[str] = mapped_column(String(100), default="Bovine Full Grain")
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    versions = relationship("ProductVersion", back_populates="family", cascade="all, delete-orphan")

class ProductVersion(Base):
    __tablename__ = "product_version"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_family_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_family.id"), nullable=False)
    version_tag: Mapped[str] = mapped_column(String(50), default="v1.0")
    materials: Mapped[dict] = mapped_column(JSONB, default=lambda: ["European Rawhide", "Vegetable Tanning Extracts"])
    finishes: Mapped[dict] = mapped_column(JSONB, default=lambda: ["Semi-aniline", "Waxed pull-up"])
    thickness_range_mm: Mapped[dict] = mapped_column(JSONB, default=lambda: ["1.2-1.4"])
    monthly_capacity_sqft: Mapped[int] = mapped_column(Integer, default=25000)
    moq_sqft: Mapped[int] = mapped_column(Integer, default=2000)
    lead_time_days: Mapped[int] = mapped_column(Integer, default=30)
    sample_lead_time_days: Mapped[int] = mapped_column(Integer, default=7)
    price_basis_inr: Mapped[float] = mapped_column(Float, default=280.0) # INR per sqft FOB
    price_basis_usd: Mapped[float] = mapped_column(Float, default=3.35)  # USD equivalent
    incoterms: Mapped[dict] = mapped_column(JSONB, default=lambda: ["FOB Chennai", "CIF Hamburg"])
    status: Mapped[str] = mapped_column(String(50), default="approved") # draft, pending_review, approved, superseded
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), default="Quality Lead")
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    family = relationship("ProductFamily", back_populates="versions")
    certificates = relationship("ProductCertificate", back_populates="version", cascade="all, delete-orphan")
    passports = relationship("ProductPassport", back_populates="version", cascade="all, delete-orphan")

class ProductCertificate(Base):
    __tablename__ = "product_certificate"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id"), nullable=False)
    cert_type: Mapped[str] = mapped_column(String(50), nullable=False) # LWG, ISO9001, REACH_TEST, CHROMIUM_VI, AZO_FREE
    certificate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    issuer: Mapped[str] = mapped_column(String(255), nullable=False)
    accredited_lab: Mapped[Optional[str]] = mapped_column(String(255), default="Eurofins / TÜV Rheinland")
    scope: Mapped[Optional[str]] = mapped_column(Text)
    file_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="verified") # verified, expired, pending, unverified
    verified_by: Mapped[Optional[str]] = mapped_column(String(100), default="Trade OS Compliance Analyst")
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    version = relationship("ProductVersion", back_populates="certificates")

class ProductPassport(Base):
    __tablename__ = "product_passport"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id"), nullable=False)
    passport_number: Mapped[str] = mapped_column(String(100), unique=True, default=lambda: f"DPP-IN-{uuid.uuid4().hex[:8].upper()}")
    status: Mapped[str] = mapped_column(String(50), default="active") # active, exported, archived
    recipient_buyer_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    passport_metadata: Mapped[dict] = mapped_column("metadata", JSONB, default=lambda: {
        "eudr_clearance": "Grade A",
        "reach_compliant": True,
        "origin": "Chennai / Ambur Leather Cluster, India",
        "qr_code_enabled": True
    })

    version = relationship("ProductVersion", back_populates="passports")
