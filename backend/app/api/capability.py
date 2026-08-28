from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import capability_repo
from app.schemas.capability import ExporterCapabilityResponse

router = APIRouter(prefix="/api/v1", tags=["Capability"])

@router.get("/capability", response_model=ExporterCapabilityResponse)
def get_capability(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    cap = capability_repo.get_exporter_capability(db)
    if not cap:
        raise HTTPException(status_code=404, detail="Exporter capability not found")

    return ExporterCapabilityResponse(
        id=str(cap.id),
        company_name=cap.company_name,
        location=cap.location,
        cluster=cap.cluster,
        export_market_focus=cap.export_market_focus or ["Germany", "EU"],
        material_types=cap.material_types or [],
        tannage=cap.tannage or [],
        thickness_range_mm=cap.thickness_range_mm or [],
        finish_capabilities=cap.finish_capabilities or [],
        monthly_capacity_sqft=cap.monthly_capacity_sqft,
        moq_sqft=cap.moq_sqft,
        lead_time_days=cap.lead_time_days,
        sample_lead_time_days=cap.sample_lead_time_days,
        port_of_export=cap.port_of_export,
        incoterms=cap.incoterms or [],
        certifications=cap.certifications or [],
        eudr_readiness_score=cap.eudr_readiness_score,
        eudr_gap_summary=cap.eudr_gap_summary
    )
