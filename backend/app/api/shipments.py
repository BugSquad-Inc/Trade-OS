import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.document import (
    ShipmentCreate,
    ShipmentMilestoneUpdate,
    ShipmentResponse
)
from app.repositories import shipment_repo

router = APIRouter(prefix="/api/v1/shipments", tags=["Ocean Shipments & eBRC Tracking"], dependencies=[Depends(require_api_key)])

@router.get("", response_model=List[ShipmentResponse])
def list_active_shipments(db: Session = Depends(get_db)):
    """List container shipments in transit with live milestones and bank eBRC payment realization."""
    return shipment_repo.list_shipments(db)

@router.post("", response_model=ShipmentResponse)
def create_shipment_tracking(shipment_in: ShipmentCreate, db: Session = Depends(get_db)):
    """Initialize a container shipment tracking record."""
    return shipment_repo.create_shipment(db, shipment_in.model_dump())

@router.get("/{shipment_id}", response_model=ShipmentResponse)
def get_shipment_details(shipment_id: uuid.UUID, db: Session = Depends(get_db)):
    """Get single shipment milestone timeline."""
    shipment = shipment_repo.get_shipment(db, shipment_id)
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found.")
    return shipment

@router.patch("/{shipment_id}/milestone", response_model=ShipmentResponse)
def update_milestone(shipment_id: uuid.UUID, update_in: ShipmentMilestoneUpdate, db: Session = Depends(get_db)):
    """Update shipment milestone and DGFT eBRC realization status."""
    shipment = shipment_repo.update_shipment_milestone(
        db,
        shipment_id=shipment_id,
        milestone=update_in.milestone,
        tracking_status=update_in.tracking_status,
        ebrc_status=update_in.ebrc_status,
        realized_amount_inr=update_in.realized_amount_inr
    )
    if not shipment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found.")
    return shipment
