from datetime import date, datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Integer, Numeric, Date, DateTime, CHAR, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class TradeLaneBenchmark(Base):
    __tablename__ = "trade_lane_benchmark"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin_country: Mapped[str] = mapped_column(CHAR(2), default="IN")
    origin_port: Mapped[str] = mapped_column(Text, default="INMAA")
    destination_country: Mapped[str] = mapped_column(CHAR(2), default="DE")
    destination_port: Mapped[str] = mapped_column(Text, default="DEHAM")
    mode: Mapped[str] = mapped_column(Text, default="sea")
    container_type: Mapped[str] = mapped_column(Text, default="40HC")
    rate_usd: Mapped[float] = mapped_column(Numeric, nullable=False)
    rate_low_usd: Mapped[float] = mapped_column(Numeric, nullable=False)
    rate_high_usd: Mapped[float] = mapped_column(Numeric, nullable=False)
    transit_days_min: Mapped[int] = mapped_column(Integer, nullable=False)
    transit_days_max: Mapped[int] = mapped_column(Integer, nullable=False)
    port_congestion_index: Mapped[str] = mapped_column(Text, default="Normal (1.2 days wait)")
    reroute_risk_notes: Mapped[Optional[str]] = mapped_column(Text)
    effective_start: Mapped[date] = mapped_column(Date, default=date.today)
    effective_end: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
