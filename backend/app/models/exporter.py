from datetime import datetime, date
import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy import Text, Integer, DateTime, Date, Boolean, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class ExporterCapability(Base):
    __tablename__ = "exporter_capability"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)
    cluster: Mapped[str] = mapped_column(Text, nullable=False)
    export_market_focus: Mapped[dict] = mapped_column(JSONB, default=lambda: ["Germany", "EU"])
    material_types: Mapped[dict] = mapped_column(JSONB, default=lambda: ["finished bovine leather", "goat nappa", "crust"])
    tannage: Mapped[dict] = mapped_column(JSONB, default=lambda: ["vegetable", "chrome", "chrome-free"])
    thickness_range_mm: Mapped[dict] = mapped_column(JSONB, default=lambda: ["0.8-1.0", "1.2-1.4", "1.6-2.2"])
    finish_capabilities: Mapped[dict] = mapped_column(JSONB, default=lambda: ["aniline", "semi-aniline", "pigmented", "pull-up"])
    monthly_capacity_sqft: Mapped[int] = mapped_column(Integer, default=50000)
    moq_sqft: Mapped[int] = mapped_column(Integer, default=3000)
    lead_time_days: Mapped[int] = mapped_column(Integer, default=35)
    sample_lead_time_days: Mapped[int] = mapped_column(Integer, default=10)
    port_of_export: Mapped[str] = mapped_column(Text, default="Chennai Port (INMAA)")
    incoterms: Mapped[dict] = mapped_column(JSONB, default=lambda: ["FOB", "CIF", "EXW"])
    certifications: Mapped[dict] = mapped_column(JSONB, default=lambda: ["LWG Gold", "ISO 9001", "ISO 14001", "REACH"])
    eudr_readiness_score: Mapped[int] = mapped_column(Integer, default=68)
    eudr_gap_summary: Mapped[Optional[str]] = mapped_column(Text)

    # India-SMB Specific Registrations & Onboarding Fields
    pan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    gstin_list: Mapped[dict] = mapped_column(JSONB, default=lambda: ["33AABCB1234F1Z1"])
    iec: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="0498765432")
    udyam_number: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="UDYAM-TN-02-0012345")
    rcmc_number: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="CLE/SR/RCMC/2024/9876")
    rcmc_expiry: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    lut_status: Mapped[Optional[str]] = mapped_column(Text, default="active") # active, expired, pending
    lut_expiry: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    ad_code: Mapped[Optional[str]] = mapped_column(Text, default="6390001")
    ad_bank_branch: Mapped[Optional[str]] = mapped_column(Text, default="State Bank of India, Overseas Branch, Chennai")
    ad_bank_ifsc: Mapped[Optional[str]] = mapped_column(Text, default="SBIN0000853")
    icegate_status: Mapped[Optional[str]] = mapped_column(Text, default="registered") # registered, pending, inactive
    authorised_signatory: Mapped[Optional[str]] = mapped_column(Text, default="K. S. Butler, Managing Director")
    facilities: Mapped[dict] = mapped_column(JSONB, default=lambda: [{"name": "Ambur Tannery Unit 1", "area_sqft": 45000, "workers": 85}])
    ports: Mapped[dict] = mapped_column(JSONB, default=lambda: ["INMAA", "INTUT"])
    incoterms_preference: Mapped[dict] = mapped_column(JSONB, default=lambda: ["FOB", "CIF", "DAP"])
    commercial_constraints: Mapped[Optional[str]] = mapped_column(Text, default="LC 60 days or 30% advance on custom tannages")

    # Workflow & Verification Tracking
    onboarding_step: Mapped[int] = mapped_column(Integer, default=5) # 1: Company, 2: Registrations, 3: Facilities, 4: Products, 5: Review
    onboarding_status: Mapped[str] = mapped_column(Text, default="approved") # draft, complete, approved, needs_review
    reviewed_by: Mapped[Optional[str]] = mapped_column(Text, default="Trade OS Senior Export Analyst")
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    evidence_status: Mapped[dict] = mapped_column(JSONB, default=lambda: {
        "pan": "verified",
        "gstin": "verified",
        "iec": "verified",
        "ad_code": "verified",
        "rcmc": "verified",
        "lut": "verified"
    })

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
