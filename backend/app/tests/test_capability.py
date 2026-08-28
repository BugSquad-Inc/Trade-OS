import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_capability_unauthorized():
    response = client.get("/api/v1/capability")
    assert response.status_code == 401

def test_capability_authorized():
    response = client.get("/api/v1/capability", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Butler's Leather"
    assert data["eudr_readiness_score"] == 68
    assert "LWG Gold Rated" in str(data["certifications"])
    assert "Chennai Port (INMAA)" in data["port_of_export"]
