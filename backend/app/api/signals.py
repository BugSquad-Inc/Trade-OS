from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import signal_repo, capability_repo
from app.services import compliance_service, lane_service
from app.schemas.signal import SignalListResponse, SignalItem

router = APIRouter(prefix="/api/v1", tags=["Signals"])

@router.get("/signals", response_model=SignalListResponse)
def get_signals_feed(
    category: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    signals = signal_repo.get_signals(db, category=category, limit=limit)
    exporter = capability_repo.get_exporter_capability(db)
    eudr = compliance_service.calculate_eudr_readiness(exporter)
    lane = lane_service.get_active_lane_benchmark(db)

    signal_items = []
    for s in signals:
        signal_items.append(SignalItem(
            id=str(s.id),
            entity_id=str(s.entity_id),
            company_name=s.company.canonical_name if s.company else "Global",
            category=s.category,
            severity=s.severity,
            title=s.title,
            summary=s.summary,
            quote=s.quote,
            source_url=s.source_url,
            detected_at=s.detected_at.isoformat() if s.detected_at else "",
            score=float(s.score),
            evidence=s.evidence or {}
        ))

    return SignalListResponse(
        signals=signal_items,
        total_count=len(signal_items),
        eudr_scorecard=eudr,
        freight_benchmark=lane
    )
