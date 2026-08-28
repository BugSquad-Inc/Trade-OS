import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_executive_kpis_endpoint():
    response = client.get("/api/v1/analytics/kpis", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert "active_exporter" in data
    assert "activation" in data
    assert "gtm" in data
    
    act = data["activation"]
    assert act["match_explainability_pct"] == 100.0
    assert act["profile_completeness_pct"] >= 90.0
    assert act["verified_contacts_count"] >= 1
    
    gtm = data["gtm"]
    assert gtm["total_buyers_monitored"] >= 5
    assert gtm["grade_a_matches"] >= 1
    assert gtm["active_signals_count"] >= 1
    assert gtm["total_customs_teu"] >= 0.0
