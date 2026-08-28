from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
import uuid
from app.models.exporter import ExporterCapability

def get_exporter_capability(db: Session) -> Optional[ExporterCapability]:
    stmt = select(ExporterCapability).limit(1)
    return db.execute(stmt).scalar_one_or_none()

def upsert_exporter_capability(db: Session, data: dict) -> ExporterCapability:
    cap = get_exporter_capability(db)
    if not cap:
        cap = ExporterCapability(**data)
        db.add(cap)
    else:
        for k, v in data.items():
            setattr(cap, k, v)
    db.commit()
    db.refresh(cap)
    return cap
