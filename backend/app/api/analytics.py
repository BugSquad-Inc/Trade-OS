from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.analytics import ExecutiveKPIDashboardResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/v1/analytics", tags=["Executive Analytics & KPIs"])

@router.get("/kpis", response_model=ExecutiveKPIDashboardResponse)
def get_executive_kpis(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    return AnalyticsService.get_executive_kpis(db)
