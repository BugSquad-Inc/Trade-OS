import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, date, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.document import ShipmentRecord, ShipmentMilestone
from app.models.company import EntityCompany

def list_shipments(db: Session) -> List[ShipmentRecord]:
    """List active and historical shipments with buyer details."""
    stmt = (
        select(ShipmentRecord)
        .options(joinedload(ShipmentRecord.buyer), joinedload(ShipmentRecord.opportunity))
        .order_by(ShipmentRecord.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())

def get_shipment(db: Session, shipment_id: uuid.UUID) -> Optional[ShipmentRecord]:
    """Get single shipment record by ID."""
    stmt = (
        select(ShipmentRecord)
        .options(joinedload(ShipmentRecord.buyer), joinedload(ShipmentRecord.opportunity))
        .where(ShipmentRecord.id == shipment_id)
    )
    return db.execute(stmt).scalar_one_or_none()

def create_shipment(db: Session, data: Dict[str, Any]) -> ShipmentRecord:
    """Create a new shipment milestone tracking record."""
    shipment = ShipmentRecord(
        tenant_id=data.get("tenant_id"),
        opportunity_id=data.get("opportunity_id"),
        buyer_id=data["buyer_id"],
        container_number=data.get("container_number", "MSKU1234567"),
        vessel_name=data.get("vessel_name", "Maersk Mc-Kinney Moller"),
        voyage_number=data.get("voyage_number", "2608W"),
        carrier=data.get("carrier", "Maersk Line"),
        origin_port=data.get("origin_port", "Chennai Port (INMAA)"),
        destination_port=data.get("destination_port", "Hamburg Port (DEHAM)"),
        etd=data.get("etd", date.today()),
        eta=data.get("eta", date.today()),
        milestone=data.get("milestone", ShipmentMilestone.vessel_departed),
        tracking_status=data.get("tracking_status", "on_time"),
        gross_weight_kg=data.get("gross_weight_kg", 14500.0),
        invoice_amount_usd=data.get("invoice_amount_usd", 45000.0),
        realized_amount_inr=data.get("realized_amount_inr", 0.0),
        ebrc_status=data.get("ebrc_status", "pending"),
        ebrc_number=data.get("ebrc_number")
    )
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment

def update_shipment_milestone(
    db: Session,
    shipment_id: uuid.UUID,
    milestone: ShipmentMilestone,
    tracking_status: Optional[str] = None,
    ebrc_status: Optional[str] = None,
    realized_amount_inr: Optional[float] = None
) -> Optional[ShipmentRecord]:
    """Update shipment transit milestone and bank eBRC realization status."""
    shipment = get_shipment(db, shipment_id)
    if not shipment:
        return None

    shipment.milestone = milestone
    if tracking_status:
        shipment.tracking_status = tracking_status
    if ebrc_status:
        shipment.ebrc_status = ebrc_status
    if realized_amount_inr is not None:
        shipment.realized_amount_inr = realized_amount_inr

    db.commit()
    db.refresh(shipment)
    return shipment
