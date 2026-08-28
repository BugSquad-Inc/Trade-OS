from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.crm import CRMExportRequest, CRMExportResponse
from app.services.crm_service import CRMExportService

router = APIRouter(prefix="/api/v1/crm", tags=["CRM & Enterprise Export"])

@router.post("/export", response_model=CRMExportResponse)
def export_buyer_crm(
    req: CRMExportRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    try:
        b_uuid = uuid.UUID(req.buyer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid buyer UUID")

    try:
        res = CRMExportService.export_buyer_dossier(db, b_uuid, export_format=req.export_format)
        return CRMExportResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
