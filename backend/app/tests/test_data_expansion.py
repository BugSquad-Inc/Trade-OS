import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.services.entity_resolution_service import normalize_company_name

client = TestClient(app)

def test_company_normalization():
    assert normalize_company_name("Picard Lederwaren GmbH & Co. KG") == "picard lederwaren"
    assert normalize_company_name("Bader GmbH & Co. KG") == "bader"
    assert normalize_company_name("Gucci S.p.A.") == "gucci"
    assert normalize_company_name("Hermès International S.A.") == "hermes international"

def test_ingest_status_endpoint():
    response = client.get("/api/v1/ingest/status", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert "active_sources" in data
    assert data["active_sources"] == 6

def test_pipeline_refresh_endpoint():
    response = client.post("/api/v1/ingest/refresh", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "succeeded"
    assert data["buyers_scored"] >= 5
    assert "duration_ms" in data

def test_matches_scaling():
    response = client.get("/api/v1/matches?limit=50", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 5
