import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_trade_corridors_list():
    response = client.get('/api/v1/lanes/corridors', headers={'X-TradeOS-Key': settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data['total_corridors'] >= 4
    
    corridors = data['corridors']
    hamburg = next(c for c in corridors if c['destination_port'] == 'DEHAM')
    assert hamburg['ocean_freight_usd_feu'] == 1850.0
    assert hamburg['landed_cost_eur_sqft'] > 0

    genoa = next(c for c in corridors if c['destination_port'] == 'ITGOA')
    assert genoa['destination_country'] == 'Italy'
    assert genoa['transit_days_min'] <= 25
