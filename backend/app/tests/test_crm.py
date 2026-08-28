import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_crm_export_hubspot():
    m_res = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    buyer = m_res.json()["matches"][0]
    buyer_id = buyer["buyer_id"]

    payload = {
        "buyer_id": buyer_id,
        "export_format": "hubspot"
    }
    response = client.post("/api/v1/crm/export", json=payload, headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "hubspot"
    assert data["status"] == "success"
    assert "company_properties" in data["payload"]
    assert "deal_proposal" in data["payload"]

def test_crm_export_csv():
    m_res = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    buyer = m_res.json()["matches"][0]
    buyer_id = buyer["buyer_id"]

    payload = {
        "buyer_id": buyer_id,
        "export_format": "csv"
    }
    response = client.post("/api/v1/crm/export", json=payload, headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "csv"
    assert "csv_content" in data["payload"]
    assert "Company Name" in data["payload"]["csv_content"]
