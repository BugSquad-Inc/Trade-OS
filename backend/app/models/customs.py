from datetime import datetime, date
import uuid
from typing import Optional
from sqlalchemy import Text, Integer, Numeric, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class CustomsShipmentNormalized(Base):
    __tablename__ = "customs_shipments_normalized"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bol_number: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    shipment_date: Mapped[date] = mapped_column(Date, nullable=False)
    importer_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="SET NULL"))
    importer_raw_name: Mapped[str] = mapped_column(Text, nullable=False)
    exporter_raw_name: Mapped[str] = mapped_column(Text, nullable=False)
    origin_country: Mapped[str] = mapped_column(Text, default="IN")
    origin_port: Mapped[str] = mapped_column(Text, default="INMAA")
    destination_country: Mapped[str] = mapped_column(Text, default="DE")
    destination_port: Mapped[str] = mapped_column(Text, default="DEHAM")
    hs_code: Mapped[str] = mapped_column(Text, nullable=False)
    product_desc: Mapped[str] = mapped_column(Text, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0)
    teu_count: Mapped[float] = mapped_column(Numeric(6, 2), default=1.0)
    declared_value_usd: Mapped[Optional[float]] = mapped_column(Numeric(14, 2))
    raw_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class CRMExportLog(Base):
    __tablename__ = "crm_export_log"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=False)
    export_format: Mapped[str] = mapped_column(Text, nullable=False)  # csv | hubspot | salesforce | webhook
    status: Mapped[str] = mapped_column(Text, default="success")
    exported_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    destination_target: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
