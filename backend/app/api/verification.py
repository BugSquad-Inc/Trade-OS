import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.verification import (
    VerificationQueueResponse,
    SignOffRequest,
    CorrectionCreate,
    CorrectionResponse,
    EntityResolutionLinkCreate,
    EntityResolutionLinkResponse
)
from app.repositories import verification_repo

router = APIRouter(prefix="/api/v1/verification", tags=["Buyer Verification & Entity Resolution"], dependencies=[Depends(require_api_key)])

@router.get("/queue", response_model=List[VerificationQueueResponse])
def get_verification_queue(status_filter: Optional[str] = Query(None, alias="status"), db: Session = Depends(get_db)):
    """Retrieve items in the research analyst verification queue."""
    return verification_repo.list_verification_queue(db, status_filter=status_filter)

@router.post("/queue/{queue_id}/sign-off", response_model=VerificationQueueResponse)
def sign_off_queue_item(queue_id: uuid.UUID, sign_off_in: SignOffRequest, db: Session = Depends(get_db)):
    """Approve or reject a buyer/signal assertion with analyst notes and evidence linkage."""
    item = verification_repo.sign_off_claim(
        db,
        queue_id=queue_id,
        approved=sign_off_in.approved,
        notes=sign_off_in.notes,
        reviewer=sign_off_in.reviewer or "Trade OS Senior Analyst"
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verification queue item not found.")
    return item

@router.post("/corrections", response_model=CorrectionResponse)
def submit_data_correction(correction_in: CorrectionCreate, db: Session = Depends(get_db)):
    """Submit a factual data correction report for an entity or contact."""
    return verification_repo.submit_correction(db, correction_in.model_dump())

@router.get("/entity-resolution", response_model=List[EntityResolutionLinkResponse])
def get_entity_resolution_links(db: Session = Depends(get_db)):
    """List entity resolution mappings (e.g. brand to parent company links)."""
    return verification_repo.list_entity_resolution_links(db)

@router.post("/entity-resolution", response_model=EntityResolutionLinkResponse)
def create_entity_resolution_mapping(link_in: EntityResolutionLinkCreate, db: Session = Depends(get_db)):
    """Create a verified brand/subsidiary linkage to parent entity."""
    return verification_repo.create_entity_resolution_link(db, link_in.model_dump())
