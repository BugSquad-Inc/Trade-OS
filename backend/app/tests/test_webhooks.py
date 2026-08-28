import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_webhook_subscription_and_dispatch():
    sub_payload = {
        'target_url': 'https://api.butlersleather.com/webhooks/tradeos',
        'events': ['MATCH_QUALIFIED', 'CUSTOMS_SHIPMENT']
    }
    response = client.post('/api/v1/webhooks/subscribe', json=sub_payload, headers={'X-TradeOS-Key': settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data['target_url'] == sub_payload['target_url']
    assert data['is_active'] is True

    # Test list
    list_res = client.get('/api/v1/webhooks', headers={'X-TradeOS-Key': settings.API_KEY})
    assert list_res.status_code == 200
    assert list_res.json()['total_count'] >= 1

    # Test dispatch
    disp_res = client.post('/api/v1/webhooks/test-dispatch?event_type=MATCH_QUALIFIED', headers={'X-TradeOS-Key': settings.API_KEY})
    assert disp_res.status_code == 200
    assert disp_res.json()['status'] == 'succeeded'
    assert disp_res.json()['dispatched_count'] >= 1
