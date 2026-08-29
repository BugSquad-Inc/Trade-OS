import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.document import (
    TradeDocumentCreate,
    TradeDocumentResponse,
    ComplianceAuditRequest,
    ComplianceAuditResponse
)
from app.repositories import document_repo
from app.services.compliance_engine_v2 import evaluate_market_compliance_v2

router = APIRouter(prefix="/api/v1/documents", tags=["Export Documents & Compliance Vault"], dependencies=[Depends(require_api_key)])

@router.get("", response_model=List[TradeDocumentResponse])
def list_export_documents(
    doc_type: Optional[str] = Query(None),
    opportunity_id: Optional[uuid.UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """List trade documents stored in the export compliance vault."""
    return document_repo.list_documents(db, doc_type=doc_type, opportunity_id=opportunity_id)

@router.post("", response_model=TradeDocumentResponse)
def upload_trade_document(doc_in: TradeDocumentCreate, db: Session = Depends(get_db)):
    """Register metadata and vault SHA-256 hash for a trade document."""
    return document_repo.create_document(db, doc_in.model_dump())

@router.post("/compliance-audit", response_model=ComplianceAuditResponse)
def audit_consignment_compliance(req: ComplianceAuditRequest):
    """Run Compliance Rule Engine v2 against EUDR, REACH SVHC, Chromium VI, and LWG standards."""
    return evaluate_market_compliance_v2(
        product_data={},
        exporter_certs=req.exporter_certs,
        has_farm_polygons=req.has_farm_polygons,
        cr_vi_tested_zero=req.cr_vi_tested_zero,
        reach_svhc_zero=req.reach_svhc_zero
    )
