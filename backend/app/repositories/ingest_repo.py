from sqlalchemy.orm import Session
from sqlalchemy import select, desc, func
from typing import List, Optional, Dict, Any
import uuid
from app.models.ingestion import SourceSystem, IngestionRun, RawDocument, RawExtract

def get_or_create_source(db: Session, name: str, kind: str, base_url: str = None, legal_basis: str = None) -> SourceSystem:
    stmt = select(SourceSystem).where(SourceSystem.name == name)
    source = db.execute(stmt).scalar_one_or_none()
    if not source:
        source = SourceSystem(
            name=name,
            kind=kind,
            base_url=base_url,
            legal_basis=legal_basis or "Public B2B directory / trade fair catalog under GDPR Art. 6(1)(f)"
        )
        db.add(source)
        db.commit()
        db.refresh(source)
    return source

def create_ingestion_run(db: Session, source_id: uuid.UUID) -> IngestionRun:
    run = IngestionRun(
        source_id=source_id,
        status="running"
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

def complete_ingestion_run(db: Session, run_id: uuid.UUID, stats: dict, status: str = "succeeded", error: str = None) -> IngestionRun:
    run = db.get(IngestionRun, run_id)
    if run:
        run.status = status
        run.finished_at = func.now()
        run.stats = stats
        run.error = error
        db.commit()
        db.refresh(run)
    return run

def list_recent_ingestion_runs(db: Session, limit: int = 20) -> List[IngestionRun]:
    stmt = select(IngestionRun).order_by(desc(IngestionRun.started_at)).limit(limit)
    return list(db.execute(stmt).scalars().all())
