from sqlalchemy.orm import Session
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
