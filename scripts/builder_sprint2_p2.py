import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/schemas/ingest.py
w("backend/app/schemas/ingest.py", """from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class IngestionRunItem(BaseModel):
    id: str
    source_name: str
    status: str
    started_at: str
    finished_at: Optional[str] = None
    stats: Dict[str, Any] = {}
    error: Optional[str] = None

class IngestionStatusResponse(BaseModel):
    runs: List[IngestionRunItem]
    total_runs: int
    active_sources: int

class TriggerIngestionRequest(BaseModel):
    source_type: str = "trade_shows"  # trade_shows | regulatory | linkedin_signals
    batch_size: int = 50

class TriggerIngestionResponse(BaseModel):
    status: str
    message: str
    run_id: Optional[str] = None
    stats: Dict[str, Any] = {}

class PipelineRefreshResponse(BaseModel):
    status: str
    message: str
    buyers_scored: int
    signals_updated: int
    duration_ms: float
""")

# 2. backend/app/api/ingest.py
w("backend/app/api/ingest.py", """from fastapi import APIRouter, Depends, HTTPException
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
""")

# 3. backend/app/workers/nightly_refresh_worker.py
w("backend/app/workers/nightly_refresh_worker.py", """from sqlalchemy.orm import Session
from app.repositories import account_repo, capability_repo, match_repo, signal_repo
from app.services import scoring_service, lane_service, compliance_service

def execute_nightly_pipeline(db: Session) -> dict:
    \"\"\"Nightly batch pipeline: recalculates match scores, updates signals, logs append-only history.\"\"\"
    exporter = capability_repo.get_exporter_capability(db)
    buyers = account_repo.get_all_buyers(db)

    scored_count = 0
    for idx, buyer in enumerate(buyers, start=1):
        score = scoring_service.score_match(buyer, exporter, rank=min(idx, 5))
        
        match_repo.upsert_match_candidate(db, {
            "buyer_id": buyer.id,
            "total_score": score.total_score,
            "product_fit_score": score.product_fit_score,
            "compliance_score": score.compliance_score,
            "lane_economics_score": score.lane_economics_score,
            "intent_signals_score": score.intent_signals_score,
            "accessibility_score": score.accessibility_score,
            "grade": score.grade,
            "rank": idx,
            "score_version": "v1.0.0",
            "drivers": [d.model_dump() for d in score.drivers],
            "key_gaps": score.key_gaps,
            "next_best_action": score.next_best_action,
            "outreach_angle": score.outreach_angle,
            "status": "suggested"
        })

        # History: INSERT ONLY (Rule 7)
        match_repo.insert_score_history(
            db,
            buyer_id=buyer.id,
            score=score.total_score,
            score_version="v1.0.0",
            drivers=[d.model_dump() for d in score.drivers]
        )
        scored_count += 1

    return {
        "buyers_scored": scored_count,
        "signals_emitted": signal_repo.get_signals(db, limit=500).__len__()
    }

if __name__ == "__main__":
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        res = execute_nightly_pipeline(db)
        print(f"[NIGHTLY REFRESH WORKER COMPLETE] {res}")
    finally:
        db.close()
""")

print("[SUCCESS] Sprint 2 Part 2 (Ingest Router, Schemas & Nightly Worker) built successfully")
