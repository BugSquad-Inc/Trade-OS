import uuid
from datetime import datetime, date, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

class DocumentType(str, Enum):
    eudr_dds = "eudr_dds"
    lab_test_report = "lab_test_report"
    commercial_invoice = "commercial_invoice"
    packing_list = "packing_list"
    bill_of_lading = "bill_of_lading"
    certificate_of_origin = "certificate_of_origin"
    rcmc_cle = "rcmc_cle"
    ebrc_certificate = "ebrc_certificate"

class ShipmentMilestone(str, Enum):
    booking_confirmed = "booking_confirmed"
    cargo_picked = "cargo_picked"
    customs_cleared_origin = "customs_cleared_origin"
    vessel_departed = "vessel_departed"
    transshipment = "transshipment"
    vessel_arrived = "vessel_arrived"
    customs_cleared_dest = "customs_cleared_dest"
    delivered = "delivered"

class TradeDocument(Base):
    __tablename__ = "trade_document"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.tenant.id"), nullable=True, index=True)
    opportunity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.opportunity.id", ondelete="SET NULL"), nullable=True, index=True)
    shipment_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    product_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id", ondelete="SET NULL"), nullable=True)

    doc_type: Mapped[DocumentType] = mapped_column(
        SQLEnum(DocumentType, name="document_type_enum", schema="gold"),
        nullable=False,
        index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=102400)
    file_hash_sha256: Mapped[str] = mapped_column(String(64), default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    mime_type: Mapped[str] = mapped_column(String(100), default="application/pdf")
    storage_uri: Mapped[str] = mapped_column(String(500), default="s3://tradeos-vault/butlers/docs/sample.pdf")
    status: Mapped[str] = mapped_column(String(50), default="verified") # draft, verified, issued, expired
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    opportunity = relationship("Opportunity")
    product_version = relationship("ProductVersion")

class ShipmentRecord(Base):
    __tablename__ = "shipment_record"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.tenant.id"), nullable=True, index=True)
    opportunity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.opportunity.id", ondelete="SET NULL"), nullable=True, index=True)
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=False, index=True)

    shipment_ref: Mapped[str] = mapped_column(String(100), unique=True, default=lambda: f"SHP-2026-{uuid.uuid4().hex[:6].upper()}")
    container_number: Mapped[str] = mapped_column(String(50), default="MSKU1234567")
    vessel_name: Mapped[str] = mapped_column(String(100), default="Maersk Mc-Kinney Moller")
    voyage_number: Mapped[str] = mapped_column(String(50), default="2608W")
    carrier: Mapped[str] = mapped_column(String(100), default="Maersk Line")
    origin_port: Mapped[str] = mapped_column(String(100), default="Chennai Port (INMAA)")
    destination_port: Mapped[str] = mapped_column(String(100), default="Hamburg Port (DEHAM)")

    etd: Mapped[date] = mapped_column(Date, default=lambda: date.today())
    eta: Mapped[date] = mapped_column(Date, default=lambda: date.today())
    milestone: Mapped[ShipmentMilestone] = mapped_column(
        SQLEnum(ShipmentMilestone, name="shipment_milestone_enum", schema="gold"),
        default=ShipmentMilestone.vessel_departed,
        nullable=False
    )
    tracking_status: Mapped[str] = mapped_column(String(50), default="on_time") # on_time, delayed, customs_hold
    gross_weight_kg: Mapped[float] = mapped_column(Float, default=14500.0)
    
    # Financial & DGFT eBRC Tracking
    invoice_amount_usd: Mapped[float] = mapped_column(Float, default=45000.0)
    realized_amount_inr: Mapped[float] = mapped_column(Float, default=0.0)
    ebrc_status: Mapped[str] = mapped_column(String(50), default="pending") # pending, applied, realized, closed
    ebrc_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    buyer = relationship("EntityCompany")
    opportunity = relationship("Opportunity")
