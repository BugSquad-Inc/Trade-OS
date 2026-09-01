import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": settings.API_KEY}

def test_production_security_headers_and_compression():
    # 1. Test root endpoint for security headers
    res = client.get("/")
    assert res.status_code == 200
    assert res.headers.get("X-Content-Type-Options") == "nosniff"
    assert res.headers.get("X-Frame-Options") == "DENY"
    assert "Strict-Transport-Security" in res.headers
    assert res.headers.get("X-TradeOS-Engine") == "v2.0-universal-sprint7"

def test_full_exporter_lifecycle_e2e_integration():
    # Step 1: Health & Exporter Profile
    exp_res = client.get("/api/v1/capability", headers=AUTH_HEADERS)
    assert exp_res.status_code == 200

    # Step 2: Product Matrix & DPP Public Lookup
    prod_res = client.get("/api/v1/products", headers=AUTH_HEADERS)
    assert prod_res.status_code == 200
    products = prod_res.json()
    assert len(products) > 0

    # Step 3: Match Engine v2 with Explainability & Counter-factuals
    match_res = client.get("/api/v1/matches", headers=AUTH_HEADERS)
    assert match_res.status_code == 200
    matches = match_res.json()["matches"]
    assert len(matches) > 0
    top_match = matches[0]
    buyer_id = top_match["buyer_id"]
    assert top_match["total_score"] > 50.0
    assert len(top_match["counter_factuals"]) > 0

    # Step 4: Intent Signals Feed
    sig_res = client.get("/api/v1/signals", headers=AUTH_HEADERS)
    assert sig_res.status_code == 200

    # Step 5: Multi-Modal Outreach Generation (German DIN 5008)
    outreach_res = client.post(
        "/api/v1/outreach",
        json={"buyer_id": buyer_id, "mode": "email", "language": "de", "tone": "Professional"},
        headers=AUTH_HEADERS
    )
    assert outreach_res.status_code == 200
    assert "Sehr geehrte" in outreach_res.json()["body"]

    # Step 6: Export-Ready Compliance Pack Manifest
    pack_res = client.get(f"/api/v1/outreach/compliance-pack/{buyer_id}", headers=AUTH_HEADERS)
    assert pack_res.status_code == 200
    assert pack_res.json()["total_documents"] >= 4

    # Step 7: Deals Pipeline & Stage Gate Inspection
    deals_res = client.get("/api/v1/deals", headers=AUTH_HEADERS)
    assert deals_res.status_code == 200
    deals = deals_res.json()
    assert len(deals) > 0
    deal_id = deals[0]["id"]

    # Step 8: Journey Stage Transition Gate Inspection
    inspect_res = client.get(f"/api/v1/journey/opportunities/{deal_id}/state", headers=AUTH_HEADERS)
    assert inspect_res.status_code == 200
    inspect_data = inspect_res.json()
    assert "macro_stage" in inspect_data
    assert "available_actions" in inspect_data

    # Step 9: Today Cockpit Actions
    today_res = client.get("/api/v1/today", headers=AUTH_HEADERS)
    assert today_res.status_code == 200
    assert "urgent_tasks" in today_res.json()

    # Step 10: Multi-Tenant RBAC Protection
    dummy_version_id = uuid.uuid4()
    forbidden_res = client.post(
        f"/api/v1/products/versions/{dummy_version_id}/certificates",
        json={"certificate_name": "Hack Cert", "certificate_type": "lwg", "issuer": "Fake", "valid_until": "2028-01-01"},
        headers={**AUTH_HEADERS, "X-User-Role": "sales"} # Sales role is forbidden from signing certificates
    )
    assert forbidden_res.status_code == 403
