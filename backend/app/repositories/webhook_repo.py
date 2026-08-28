from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Dict, Any
import uuid
import secrets
from app.models.webhook import WebhookSubscription, WebhookEventLog

def create_subscription(db: Session, target_url: str, events: List[str]) -> WebhookSubscription:
    sub = WebhookSubscription(
        id=uuid.uuid4(),
        target_url=target_url,
        secret_key=secrets.token_hex(24),
        events=events,
        is_active=True
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

def list_subscriptions(db: Session) -> List[WebhookSubscription]:
    stmt = select(WebhookSubscription).where(WebhookSubscription.is_active == True).order_by(desc(WebhookSubscription.created_at))
    return list(db.execute(stmt).scalars().all())

def log_dispatch(db: Session, sub_id: uuid.UUID, event_type: str, payload: Dict[str, Any], status: int = 200) -> WebhookEventLog:
    log = WebhookEventLog(
        id=uuid.uuid4(),
        subscription_id=sub_id,
        event_type=event_type,
        payload=payload,
        response_status=status
    )
    db.add(log)
    db.commit()
    return log
