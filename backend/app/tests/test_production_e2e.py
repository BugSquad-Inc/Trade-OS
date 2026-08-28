import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_production_readiness_e2e():
    # 1. Health
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    # 2. Exporter Capability
    cap = client.get("/api/v1/capability", headers={"X-TradeOS-Key": settings.API_KEY})
    assert cap.status_code == 200
    assert cap.json()["company_name"] == "Butler's Leather"

    # 3. Matches
    matches = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    assert matches.status_code == 200
    assert len(matches.json()["matches"]) >= 5

    # 4. Signals
    signals = client.get("/api/v1/signals", headers={"X-TradeOS-Key": settings.API_KEY})
    assert signals.status_code == 200
    assert len(signals.json()["signals"]) >= 5

    # 5. Customs
    customs = client.get("/api/v1/customs/shipments", headers={"X-TradeOS-Key": settings.API_KEY})
    assert customs.status_code == 200
    assert customs.json()["total_count"] >= 5

    # 6. Analytics
    analytics = client.get("/api/v1/analytics/kpis", headers={"X-TradeOS-Key": settings.API_KEY})
    assert analytics.status_code == 200
    assert analytics.json()["activation"]["match_explainability_pct"] == 100.0

    # 7. Lanes
    lanes = client.get("/api/v1/lanes/corridors", headers={"X-TradeOS-Key": settings.API_KEY})
    assert lanes.status_code == 200
    assert lanes.json()["total_corridors"] >= 4

    # 8. Webhooks
    webhooks = client.get("/api/v1/webhooks", headers={"X-TradeOS-Key": settings.API_KEY})
    assert webhooks.status_code == 200
