from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, delete
from typing import List, Optional
import uuid
from app.models.match import MatchCandidate, MatchScoreHistory, MatchProfile
from app.models.company import EntityCompany

def get_match_candidates(db: Session, limit: int = 10) -> List[MatchCandidate]:
    stmt = (
        select(MatchCandidate)
        .options(
            joinedload(MatchCandidate.company).joinedload(EntityCompany.persons),
            joinedload(MatchCandidate.company).joinedload(EntityCompany.certifications)
        )
        .order_by(MatchCandidate.rank.asc(), MatchCandidate.total_score.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().unique().all())

def get_match_by_buyer_id(db: Session, buyer_id: uuid.UUID) -> Optional[MatchCandidate]:
    stmt = select(MatchCandidate).where(MatchCandidate.buyer_id == buyer_id).options(joinedload(MatchCandidate.company))
    return db.execute(stmt).scalar_one_or_none()

def upsert_match_candidate(db: Session, candidate_data: dict) -> MatchCandidate:
    buyer_id = candidate_data["buyer_id"]
    candidate = db.execute(select(MatchCandidate).where(MatchCandidate.buyer_id == buyer_id)).scalar_one_or_none()
    if not candidate:
        candidate = MatchCandidate(**candidate_data)
        db.add(candidate)
    else:
        for k, v in candidate_data.items():
            setattr(candidate, k, v)
    db.commit()
    db.refresh(candidate)
    return candidate

def insert_score_history(db: Session, buyer_id: uuid.UUID, score: float, score_version: str, drivers: list) -> MatchScoreHistory:
    history = MatchScoreHistory(
        buyer_id=buyer_id,
        score=score,
        score_version=score_version,
        drivers=drivers
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history
