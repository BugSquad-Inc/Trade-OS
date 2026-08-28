from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Integer, DateTime, func
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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
