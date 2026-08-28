import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_signals_endpoint():
    response = client.get("/api/v1/signals", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 5
    assert "eudr_scorecard" in data
    assert data["eudr_scorecard"]["readiness_score"] == 68
    assert "freight_benchmark" in data
    assert data["freight_benchmark"]["rate_usd"] == 1850.0
