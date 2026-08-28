from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class WebhookSubscribeRequest(BaseModel):
    target_url: str
    events: List[str] = ['MATCH_QUALIFIED', 'CUSTOMS_SHIPMENT', 'SIGNAL_ALERT']

class WebhookSubscriptionItem(BaseModel):
    id: str
    target_url: str
    events: List[str]
    is_active: bool
    created_at: str

class WebhookListResponse(BaseModel):
    total_count: int
    subscriptions: List[WebhookSubscriptionItem]

class WebhookDispatchResponse(BaseModel):
    event_type: str
    dispatched_count: int
    status: str
