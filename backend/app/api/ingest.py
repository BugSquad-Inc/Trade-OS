from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import ingest_repo, account_repo
from app.schemas.ingest import IngestionStatusResponse, IngestionRunItem, TriggerIngestionRequest, TriggerIngestionResponse, PipelineRefreshResponse
from app.workers.nightly_refresh_worker import execute_nightly_pipeline

router = APIRouter(prefix="/api/v1/ingest", tags=["Ingestion & Pipeline"])

@router.get("/status", response_model=IngestionStatusResponse)
def get_ingestion_status(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    runs = ingest_repo.list_recent_ingestion_runs(db, limit=20)
    items = [
        IngestionRunItem(
            id=str(r.id),
            source_name=r.source_id and str(r.source_id) or "Pipeline",
            status=r.status,
            started_at=r.started_at.isoformat() if r.started_at else "",
            finished_at=r.finished_at.isoformat() if r.finished_at else None,
            stats=r.stats or {},
            error=r.error
        ) for r in runs
    ]
    return IngestionStatusResponse(
        runs=items,
        total_runs=len(items),
        active_sources=6
    )

@router.post("/refresh", response_model=PipelineRefreshResponse)
def trigger_pipeline_refresh(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    start = time.time()
    res = execute_nightly_pipeline(db)
    duration = round((time.time() - start) * 1000, 2)

    return PipelineRefreshResponse(
        status="succeeded",
        message="Trade OS multi-source pipeline and 100-point scoring refresh completed.",
        buyers_scored=res.get("buyers_scored", 0),
        signals_updated=res.get("signals_emitted", 0),
        duration_ms=duration
    )
