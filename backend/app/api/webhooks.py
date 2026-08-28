from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import webhook_repo
from app.services.webhook_service import WebhookDispatcherService
from app.schemas.webhook import WebhookSubscribeRequest, WebhookListResponse, WebhookSubscriptionItem, WebhookDispatchResponse

router = APIRouter(prefix='/api/v1/webhooks', tags=['Webhooks and Event Automation'])

@router.post('/subscribe', response_model=WebhookSubscriptionItem)
def subscribe_webhook(
    req: WebhookSubscribeRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    sub = webhook_repo.create_subscription(db, req.target_url, req.events)
    return WebhookSubscriptionItem(
        id=str(sub.id),
        target_url=sub.target_url,
        events=sub.events or [],
        is_active=sub.is_active,
        created_at=sub.created_at.isoformat()
    )

@router.get('', response_model=WebhookListResponse)
def list_webhooks(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    subs = webhook_repo.list_subscriptions(db)
    items = [
        WebhookSubscriptionItem(
            id=str(s.id),
            target_url=s.target_url,
            events=s.events or [],
            is_active=s.is_active,
            created_at=s.created_at.isoformat()
        ) for s in subs
    ]
    return WebhookListResponse(total_count=len(items), subscriptions=items)

@router.post('/test-dispatch', response_model=WebhookDispatchResponse)
def test_webhook_dispatch(
    event_type: str = 'MATCH_QUALIFIED',
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    count = WebhookDispatcherService.dispatch_event(db, event_type, {
        'sample': 'Trade OS Event Simulation',
        'status': 'VERIFIED'
    })
    return WebhookDispatchResponse(
        event_type=event_type,
        dispatched_count=count,
        status='succeeded'
    )
