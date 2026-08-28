from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import customs_repo
from app.schemas.customs import CustomsShipmentsListResponse, CustomsShipmentItem, IngestCustomsRequest
from app.services.customs_service import CustomsIntelligenceService

router = APIRouter(prefix="/api/v1/customs", tags=["Customs & BOL Flows"])

@router.get("/shipments", response_model=CustomsShipmentsListResponse)
def get_customs_shipments(
    importer_id: Optional[str] = None,
    hs_code: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    imp_uuid = uuid.UUID(importer_id) if importer_id else None
    shipments = customs_repo.list_customs_shipments(db, importer_id=imp_uuid, hs_code=hs_code, limit=limit)
    items = [
        CustomsShipmentItem(
            id=str(s.id),
            bol_number=s.bol_number,
            shipment_date=s.shipment_date.isoformat(),
            importer_name=s.importer_raw_name,
            exporter_name=s.exporter_raw_name,
            origin_port=s.origin_port,
            destination_port=s.destination_port,
            hs_code=s.hs_code,
            product_desc=s.product_desc,
            weight_kg=float(s.weight_kg),
            teu_count=float(s.teu_count),
            declared_value_usd=float(s.declared_value_usd) if s.declared_value_usd else None
        ) for s in shipments
    ]
    return CustomsShipmentsListResponse(total_count=len(items), shipments=items)

@router.post("/ingest")
def ingest_customs_records(
    req: IngestCustomsRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    res = CustomsIntelligenceService.ingest_bol_records(db, req.bol_records)
    return {"status": "succeeded", "stats": res}
