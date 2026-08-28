import hmac
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories import webhook_repo

class WebhookDispatcherService:
    @staticmethod
    def dispatch_event(db: Session, event_type: str, payload: Dict[str, Any]) -> int:
        subs = webhook_repo.list_subscriptions(db)
        dispatched = 0

        for sub in subs:
            if event_type in (sub.events or []):
                secret = sub.secret_key.encode('utf-8')
                body = json.dumps(payload, default=str).encode('utf-8')
                signature = hmac.new(secret, body, hashlib.sha256).hexdigest()

                webhook_repo.log_dispatch(db, sub.id, event_type, {
                    'event': event_type,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'signature': f'sha256={signature}',
                    'payload': payload
                }, status=200)
                dispatched += 1

        return dispatched
