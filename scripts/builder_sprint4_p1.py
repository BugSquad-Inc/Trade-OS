import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/models/customs.py
w("backend/app/models/customs.py", """from datetime import datetime, date
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
    destination_target: Optional[Mapped[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
""")

# 2. backend/app/repositories/customs_repo.py
w("backend/app/repositories/customs_repo.py", """from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Optional, Dict, Any
import uuid
from app.models.customs import CustomsShipmentNormalized

def insert_customs_shipment(db: Session, data: Dict[str, Any]) -> CustomsShipmentNormalized:
    stmt = select(CustomsShipmentNormalized).where(CustomsShipmentNormalized.bol_number == data["bol_number"])
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        return existing
    shipment = CustomsShipmentNormalized(**data)
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment

def list_customs_shipments(db: Session, importer_id: Optional[uuid.UUID] = None, hs_code: Optional[str] = None, limit: int = 50) -> List[CustomsShipmentNormalized]:
    stmt = select(CustomsShipmentNormalized)
    if importer_id:
        stmt = stmt.where(CustomsShipmentNormalized.importer_id == importer_id)
    if hs_code:
        stmt = stmt.where(CustomsShipmentNormalized.hs_code.startswith(hs_code))
    stmt = stmt.order_by(desc(CustomsShipmentNormalized.shipment_date)).limit(limit)
    return list(db.execute(stmt).scalars().all())
""")

# 3. backend/app/repositories/crm_repo.py
w("backend/app/repositories/crm_repo.py", """from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Dict, Any
import uuid
from app.models.customs import CRMExportLog

def log_crm_export(db: Session, buyer_id: uuid.UUID, export_format: str, exported_data: Dict[str, Any], destination_target: str = None) -> CRMExportLog:
    log_entry = CRMExportLog(
        id=uuid.uuid4(),
        buyer_id=buyer_id,
        export_format=export_format,
        status="success",
        exported_data=exported_data,
        destination_target=destination_target
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def list_recent_crm_exports(db: Session, limit: int = 20) -> List[CRMExportLog]:
    stmt = select(CRMExportLog).order_by(desc(CRMExportLog.created_at)).limit(limit)
    return list(db.execute(stmt).scalars().all())
""")

print("[SUCCESS] Phase 4 Part 1 (Customs & CRM ORM Models and Repositories) built successfully")
