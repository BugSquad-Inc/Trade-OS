from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.provenance import SourceRegistry, EvidenceAssertion, TruthStatus, SourceTier

client = TestClient(app)

def test_health_endpoints():
    # 1. Base Health
    res_base = client.get("/api/v1/health")
    assert res_base.status_code == 200
    data_base = res_base.json()
    assert data_base["status"] in ("ok", "degraded")
    assert "environment" in data_base

    # 2. Liveness
    res_live = client.get("/api/v1/health/live")
    assert res_live.status_code == 200
    data_live = res_live.json()
    assert data_live["status"] == "live"
    assert data_live["uptime"] == "healthy"

    # 3. Readiness
    res_ready = client.get("/api/v1/health/ready")
    assert res_ready.status_code == 200
    data_ready = res_ready.json()
    assert data_ready["status"] == "ready"
    assert data_ready["dependencies"]["database"] == "ready"

def test_provenance_data_integrity():
    # Verify provenance tables have records
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        sources = db.query(SourceRegistry).all()
        assert len(sources) >= 1
        assert sources[0].source_tier in (SourceTier.tier_e, SourceTier.tier_a, SourceTier.tier_b)

        assertions = db.query(EvidenceAssertion).all()
        assert len(assertions) >= 1
        assert assertions[0].truth_status in (TruthStatus.demo, TruthStatus.verified)
    finally:
        db.close()
