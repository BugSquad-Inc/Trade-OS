from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
import uuid
from app.models.match import Action

def log_outreach_action(db: Session, buyer_id: uuid.UUID, action_type: str, payload: dict) -> Action:
    action = Action(
        buyer_id=buyer_id,
        action_type=action_type,
        status="generated",
        payload=payload
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

def get_outreach_history(db: Session, buyer_id: uuid.UUID) -> List[Action]:
    stmt = select(Action).where(Action.buyer_id == buyer_id).order_by(Action.created_at.desc())
    return list(db.execute(stmt).scalars().all())
