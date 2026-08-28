from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import Text, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Signal(Base):
    __tablename__ = "signal"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(Text, default="medium")
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    quote: Mapped[Optional[str]] = mapped_column(Text)
    source_url: Mapped[Optional[str]] = mapped_column(Text)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    score: Mapped[float] = mapped_column(Numeric, default=0)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="signals")
    evidence_items: Mapped[List["SignalEvidence"]] = relationship("SignalEvidence", back_populates="signal", cascade="all, delete-orphan")

class SignalEvidence(Base):
    __tablename__ = "signal_evidence"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.signal.id", ondelete="CASCADE"), nullable=False)
    document_url: Mapped[Optional[str]] = mapped_column(Text)
    quote: Mapped[Optional[str]] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Numeric, default=0.9)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    signal: Mapped["Signal"] = relationship("Signal", back_populates="evidence_items")
