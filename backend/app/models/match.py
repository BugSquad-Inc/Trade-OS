from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import Text, Integer, Numeric, Boolean, DateTime, ForeignKey, CHAR, BigInteger, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class MatchProfile(Base):
    __tablename__ = "match_profile"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    exporter_capability_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.exporter_capability.id"))
    objective: Mapped[str] = mapped_column(Text, default="find_buyers")
    criteria: Mapped[dict] = mapped_column(JSONB, default=dict)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    candidates: Mapped[List["MatchCandidate"]] = relationship("MatchCandidate", back_populates="profile", cascade="all, delete-orphan")

class MatchCandidate(Base):
    __tablename__ = "match_candidate"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.match_profile.id", ondelete="CASCADE"))
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    product_fit_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    compliance_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    lane_economics_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    intent_signals_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    accessibility_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    grade: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    score_version: Mapped[str] = mapped_column(Text, default="v1.0.0")
    drivers: Mapped[dict] = mapped_column(JSONB, default=list)
    key_gaps: Mapped[dict] = mapped_column(JSONB, default=list)
    next_best_action: Mapped[str] = mapped_column(Text, nullable=False)
    outreach_angle: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, default="suggested")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    profile: Mapped[Optional["MatchProfile"]] = relationship("MatchProfile", back_populates="candidates")
    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="match_candidate")

class MatchScoreHistory(Base):
    __tablename__ = "match_score_history"
    __table_args__ = {"schema": "gold"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    score_version: Mapped[str] = mapped_column(Text, nullable=False)
    drivers: Mapped[dict] = mapped_column(JSONB, nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class Action(Base):
    __tablename__ = "actions"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    action_type: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, default="generated")
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class AuditEvent(Base):
    __tablename__ = "audit_event"
    __table_args__ = {"schema": "audit"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    object_type: Mapped[str] = mapped_column(Text, nullable=False)
    object_id: Mapped[Optional[str]] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
