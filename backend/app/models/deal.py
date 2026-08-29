import uuid
from datetime import datetime, date, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

class OpportunityStage(str, Enum):
    matched = "matched"
    pitch_drafted = "pitch_drafted"
    outreach_sent = "outreach_sent"
    reply_positive = "reply_positive"
    sample_requested = "sample_requested"
    sample_sent = "sample_sent"
    sample_approved = "sample_approved"
    quote_sent = "quote_sent"
    contract_negotiation = "contract_negotiation"
    po_received = "po_received"
    in_production = "in_production"
    closed_won = "closed_won"
    closed_lost = "closed_lost"

class Opportunity(Base):
    __tablename__ = "opportunity"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=False, index=True)
    product_family_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_family.id"), nullable=True)
    product_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id"), nullable=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    stage: Mapped[OpportunityStage] = mapped_column(
        SQLEnum(OpportunityStage, name="opportunity_stage_enum", schema="gold"),
        default=OpportunityStage.matched,
        nullable=False,
        index=True
    )
    deal_value_eur: Mapped[float] = mapped_column(Float, default=0.0)
    deal_value_inr: Mapped[float] = mapped_column(Float, default=0.0)
    volume_sqft: Mapped[int] = mapped_column(Integer, default=5000)
    incoterms: Mapped[str] = mapped_column(String(50), default="CIF Hamburg")
    target_close_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    probability: Mapped[float] = mapped_column(Float, default=0.3)
    owner: Mapped[str] = mapped_column(String(100), default="Sales Lead")
    loss_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    buyer = relationship("EntityCompany")
    product_family = relationship("ProductFamily")
    product_version = relationship("ProductVersion")
    quotes = relationship("Quote", back_populates="opportunity", cascade="all, delete-orphan")
    tasks = relationship("TaskItem", back_populates="opportunity", cascade="all, delete-orphan")

class Quote(Base):
    __tablename__ = "quote"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.opportunity.id", ondelete="CASCADE"), nullable=False, index=True)
    quote_number: Mapped[str] = mapped_column(String(100), unique=True, default=lambda: f"QT-2026-{uuid.uuid4().hex[:6].upper()}")
    product_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.product_version.id"), nullable=True)
    freight_lane_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.trade_lane_benchmark.id"), nullable=True)

    quantity_sqft: Mapped[int] = mapped_column(Integer, default=5000)
    unit_price_inr: Mapped[float] = mapped_column(Float, default=295.0) # Base Ex-Factory / FOB INR/sqft
    unit_price_eur: Mapped[float] = mapped_column(Float, default=3.20)  # Converted base EUR/sqft
    fx_rate_eur_inr: Mapped[float] = mapped_column(Float, default=92.5) # EUR to INR exchange rate

    # Landed Cost Components
    estimated_freight_usd: Mapped[float] = mapped_column(Float, default=1850.0) # Container / air freight
    customs_duty_pct: Mapped[float] = mapped_column(Float, default=0.0) # EU import duty % (0% for crust/finished under trade arrangements)
    insurance_usd: Mapped[float] = mapped_column(Float, default=120.0)
    landed_cost_eur_per_sqft: Mapped[float] = mapped_column(Float, default=3.55)
    gross_margin_pct: Mapped[float] = mapped_column(Float, default=28.5)
    total_quote_value_eur: Mapped[float] = mapped_column(Float, default=17750.0)

    payment_terms: Mapped[str] = mapped_column(String(255), default="30% Advance, 70% against Copy of Bill of Lading")
    lead_time_days: Mapped[int] = mapped_column(Integer, default=30)
    status: Mapped[str] = mapped_column(String(50), default="sent") # draft, sent, accepted, revised, expired
    valid_until: Mapped[date] = mapped_column(Date, default=lambda: date.today())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    opportunity = relationship("Opportunity", back_populates="quotes")
    product_version = relationship("ProductVersion")
    freight_lane = relationship("TradeLaneBenchmark")

class TaskItem(Base):
    __tablename__ = "task_item"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.opportunity.id", ondelete="CASCADE"), nullable=True, index=True)
    buyer_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    due_date: Mapped[date] = mapped_column(Date, default=lambda: date.today())
    priority: Mapped[str] = mapped_column(String(20), default="high") # urgent, high, medium, low
    status: Mapped[str] = mapped_column(String(50), default="todo") # todo, in_progress, completed
    task_type: Mapped[str] = mapped_column(String(50), default="outreach_approval") # sample_dispatch, quote_followup, outreach_approval, dds_upload
    assigned_to: Mapped[str] = mapped_column(String(100), default="Sales Lead")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    opportunity = relationship("Opportunity", back_populates="tasks")
    buyer = relationship("EntityCompany")
