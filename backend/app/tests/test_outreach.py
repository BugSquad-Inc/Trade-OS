import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_outreach_generation():
    m_res = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    buyer = m_res.json()["matches"][0]
    buyer_id = buyer["buyer_id"]

    payload = {
        "buyer_id": buyer_id,
        "tone": "Professional"
    }

    response = client.post("/api/v1/outreach", json=payload, headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["buyer_name"] == buyer["name"]
    assert data["tone"] == "Professional"
    assert "EUDR" in data["subject"]
    assert "Butler's Leather" in data["body"]
    assert "Chennai" in data["body"]
