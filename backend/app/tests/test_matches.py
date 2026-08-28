import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_matches_unauthorized():
    response = client.get("/api/v1/matches")
    assert response.status_code == 401

def test_matches_authorized():
    response = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 5
    assert len(data["matches"]) == 5

    top_match = data["matches"][0]
    assert top_match["rank"] == 1
    assert top_match["name"] == "Picard GmbH"
    assert top_match["grade"] == "A"
    assert top_match["total_score"] >= 85.0
    assert len(top_match["drivers"]) == 5
    assert top_match["contact"]["verification_status"] == "verified"
