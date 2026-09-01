from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.api.deps import require_api_key
from app.services import outreach_service
from app.schemas.outreach import OutreachRequest, OutreachResponse, CompliancePackResponse

router = APIRouter(prefix="/api/v1", tags=["Outreach"])

@router.post("/outreach", response_model=OutreachResponse)
def generate_outreach(
    req: OutreachRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    try:
        buyer_uuid = uuid.UUID(req.buyer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid buyer UUID format")

    try:
        res = outreach_service.generate_personalized_outreach(
            db,
            buyer_id=buyer_uuid,
            mode=req.mode,
            language=req.language,
            tone=req.tone,
            contact_name=req.contact_name
        )
        return OutreachResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/outreach/compliance-pack/{buyer_id}", response_model=CompliancePackResponse)
def get_buyer_compliance_pack(
    buyer_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    """
    Generate downloadable export-ready compliance pack bundle manifest for EU buyers.
    """
    try:
        buyer_uuid = uuid.UUID(buyer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid buyer UUID format")

    try:
        return outreach_service.generate_compliance_pack(db, buyer_id=buyer_uuid)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
