import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_customs_shipments_list():
    response = client.get("/api/v1/customs/shipments", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert "shipments" in data
    assert data["total_count"] >= 1
    s = data["shipments"][0]
    assert "bol_number" in s
    assert "origin_port" in s
    assert "destination_port" in s
    assert "hs_code" in s
    assert s["weight_kg"] > 0
