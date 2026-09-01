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
    specifications = relationship("ProductSpecification", back_populates="version", cascade="all, delete-orphan", uselist=False)
    chemical_spec = relationship("ChemicalComplianceSpec", back_populates="version", cascade="all, delete-orphan", uselist=False)
    traceability_spec = relationship("TraceabilitySpec", back_populates="version", cascade="all, delete-orphan", uselist=False)
    certificates = relationship("ProductCertificate", back_populates="version", cascade="all, delete-orphan")
    passports = relationship("ProductPassport", back_populates="version", cascade="all, delete-orphan")

class ProductSpecification(Base):
    """Physical technical parameters for leather articles."""
    __tablename__ = "product_specification"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id"), nullable=False, unique=True)
    thickness_min_mm: Mapped[float] = mapped_column(Float, default=1.2)
    thickness_max_mm: Mapped[float] = mapped_column(Float, default=1.4)
    temper: Mapped[str] = mapped_column(String(50), default="medium_soft") # soft, medium_soft, firm
    tensile_strength_n_per_mm2: Mapped[float] = mapped_column(Float, default=15.0)
    tear_strength_n: Mapped[float] = mapped_column(Float, default=40.0)
    grain_type: Mapped[str] = mapped_column(String(100), default="Full Grain Natural Mill")
    tannage_type: Mapped[str] = mapped_column(String(100), default="Chrome-Free Synthetic / Veg Retan")
    origin_country: Mapped[str] = mapped_column(String(50), default="India")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    version = relationship("ProductVersion", back_populates="specifications")

class ChemicalComplianceSpec(Base):
    """REACH and EU chemical limits per batch/spec."""
    __tablename__ = "chemical_compliance_spec"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id"), nullable=False, unique=True)
    chromium_vi_ppm: Mapped[float] = mapped_column(Float, default=0.0) # Must be < 3.0 ppm per DIN EN ISO 17075
    azo_dyes_ppm: Mapped[float] = mapped_column(Float, default=0.0) # Must be < 30.0 ppm
    formaldehyde_ppm: Mapped[float] = mapped_column(Float, default=12.0) # Must be < 75.0 ppm
    pfas_free: Mapped[bool] = mapped_column(Boolean, default=True)
    reach_svhc_status: Mapped[str] = mapped_column(String(50), default="compliant") # compliant, non_compliant, tested
    lab_test_report_id: Mapped[Optional[str]] = mapped_column(String(100), default="TR-TUV-2026-8812")
    accredited_lab: Mapped[str] = mapped_column(String(100), default="TÜV Rheinland / Eurofins")
    test_date: Mapped[date] = mapped_column(Date, default=lambda: date.today())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    version = relationship("ProductVersion", back_populates="chemical_spec")

class TraceabilitySpec(Base):
    """EUDR and Abattoir origin geolocation records."""
    __tablename__ = "traceability_spec"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id"), nullable=False, unique=True)
    abattoir_license_no: Mapped[str] = mapped_column(String(100), default="APEDA-TN-7821")
    mandal_district: Mapped[str] = mapped_column(String(100), default="Ambur / Tirupattur District")
    state: Mapped[str] = mapped_column(String(50), default="Tamil Nadu")
    geolocation_lat: Mapped[float] = mapped_column(Float, default=12.7904)
    geolocation_lng: Mapped[float] = mapped_column(Float, default=78.7163)
    eudr_cutoff_cleared: Mapped[bool] = mapped_column(Boolean, default=True) # Proven post-2020 legal land use
    hide_origin_batch: Mapped[str] = mapped_column(String(100), default="BATCH-2026-TN-04")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    version = relationship("ProductVersion", back_populates="traceability_spec")

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
    public_token: Mapped[str] = mapped_column(String(64), unique=True, default=lambda: f"tok_{uuid.uuid4().hex[:16]}")
    qr_code_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    carbon_footprint_kg_co2e: Mapped[float] = mapped_column(Float, default=4.2) # kg CO2e per sqft finished leather
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
