from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Boolean, DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class SourceSystem(Base):
    __tablename__ = "source_system"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    base_url: Mapped[Optional[str]] = mapped_column(Text)
    legal_basis: Mapped[Optional[str]] = mapped_column(Text)
    robots_policy: Mapped[Optional[str]] = mapped_column(Text)
    auth: Mapped[dict] = mapped_column(JSONB, default=dict)
    rate_limit: Mapped[dict] = mapped_column(JSONB, default=lambda: {"requests_per_minute": 30})
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

class IngestionRun(Base):
    __tablename__ = "ingestion_run"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bronze.source_system.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(Text, default="queued")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    cursor: Mapped[Optional[str]] = mapped_column(Text)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)
    error: Mapped[Optional[str]] = mapped_column(Text)

class RawDocument(Base):
    __tablename__ = "raw_document"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bronze.source_system.id"), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(Text)
    mime_type: Mapped[Optional[str]] = mapped_column(Text)
    content_text: Mapped[Optional[str]] = mapped_column(Text)
    content_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    content_hash: Mapped[str] = mapped_column(Text, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    meta: Mapped[dict] = mapped_column(JSONB, default=dict)

class RawExtract(Base):
    __tablename__ = "raw_extract"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bronze.raw_document.id", ondelete="CASCADE"), nullable=False)
    extractor_name: Mapped[str] = mapped_column(Text, nullable=False)
    extractor_version: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, default="success")
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    confidence: Mapped[float] = mapped_column(Numeric, default=0.9)
    error: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
