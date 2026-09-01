import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key, require_role
from app.models.tenant import UserRole
from app.models.company import EntityCompany
from app.models.provenance import TruthStatus
from app.schemas.verification import (
    VerificationQueueResponse,
    SignOffRequest,
    AnalystReviewRequest,
    FreshnessCheckResponse,
    CorrectionCreate,
    CorrectionResponse,
    EntityResolutionLinkCreate,
    EntityResolutionLinkResponse
)
from app.repositories import verification_repo
from app.services import provenance_service

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

@router.post("/queue/{queue_id}/review", response_model=VerificationQueueResponse, dependencies=[Depends(require_role([UserRole.owner, UserRole.analyst, UserRole.compliance]))])
def review_queue_item(
    queue_id: uuid.UUID,
    review_in: AnalystReviewRequest,
    db: Session = Depends(get_db)
):
    """
    Process analyst review: 'approve', 'reject', or 'dispute' with attached evidence document.
    """
    try:
        return provenance_service.execute_analyst_review(
            db=db,
            queue_id=queue_id,
            decision=review_in.decision,
            notes=review_in.notes,
            evidence_reference=review_in.evidence_reference,
            reviewer=review_in.reviewer or "Trade OS Senior Research Analyst"
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/freshness/{company_id}", response_model=FreshnessCheckResponse)
def check_company_freshness(company_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Compute data freshness against the 90-day SLA and calculate effective truth status.
    """
    comp = db.query(EntityCompany).filter(EntityCompany.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company entity not found.")

    base_status = TruthStatus(comp.truth_status) if comp.truth_status in [e.value for e in TruthStatus] else TruthStatus.demo
    effective_status, is_stale, label = provenance_service.resolve_effective_truth_status(
        base_status=base_status,
        checked_at=comp.checked_at
    )
    _, days_old, _ = provenance_service.calculate_freshness(comp.checked_at)

    return FreshnessCheckResponse(
        entity_id=comp.id,
        is_stale=is_stale,
        days_old=days_old,
        freshness_label=label,
        effective_truth_status=effective_status.value
    )

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
