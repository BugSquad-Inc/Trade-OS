import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_account_360_detail():
    m_res = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    top_buyer = m_res.json()["matches"][0]
    buyer_id = top_buyer["buyer_id"]

    response = client.get(f"/api/v1/accounts/{buyer_id}", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_name"] == top_buyer["name"]
    assert len(data["contacts"]) >= 1
    contact = data["contacts"][0]
    assert contact["legal_basis"] == "B2B legitimate interest under GDPR Art. 6(1)(f)"
    assert contact["confidence"] >= 0.8
    assert len(data["eudr_requirements"]) >= 4
    assert "lane_economics" in data
