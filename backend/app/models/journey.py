import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, DateTime, Text, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class JourneyMacroStage(str, Enum):
    get_ready = "get_ready"
    find_buyers = "find_buyers"
    connect = "connect"
    sample_and_quote = "sample_and_quote"
    fulfil_order = "fulfil_order"
    ship = "ship"
    get_paid = "get_paid"
    repeat = "repeat"

class StageEvent(Base):
    """
    Immutable, append-only record of journey state transitions and decisions.
    Never update or delete historical records.
    """
    __tablename__ = "stage_events"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # opportunity, shipment, invoice
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    
    macro_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    previous_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    new_stage: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    
    actor: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. Johann Butler (Owner)
    actor_role: Mapped[str] = mapped_column(String(50), default="owner")
    reason_code: Mapped[str] = mapped_column(String(100), default="workflow_progression")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    evidence_references: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(128), nullable=True, index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
