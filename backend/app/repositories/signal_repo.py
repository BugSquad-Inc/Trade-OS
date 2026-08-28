from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from typing import List, Optional
import uuid
from app.models.signal import Signal, SignalEvidence

def get_signals(db: Session, category: Optional[str] = None, limit: int = 50) -> List[Signal]:
    stmt = select(Signal).options(joinedload(Signal.company)).order_by(Signal.detected_at.desc())
    if category:
        stmt = stmt.where(Signal.category == category)
    stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars().all())

def get_signals_for_entity(db: Session, entity_id: uuid.UUID) -> List[Signal]:
    stmt = select(Signal).where(Signal.entity_id == entity_id).order_by(Signal.detected_at.desc())
    return list(db.execute(stmt).scalars().all())

def insert_signal(db: Session, signal_data: dict) -> Signal:
    signal = Signal(**signal_data)
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal
