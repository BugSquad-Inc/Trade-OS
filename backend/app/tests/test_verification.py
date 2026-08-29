import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": "tradeos_pilot_secret_key_2026"}

def test_verification_queue_and_sign_off():
    # 1. Fetch Verification Queue
    res = client.get("/api/v1/verification/queue", headers=AUTH_HEADERS)
    assert res.status_code == 200
    queue = res.json()
    assert len(queue) >= 1
    
    item = queue[0]
    assert "entity_name" in item
    assert "claim_type" in item
    assert "status" in item
    queue_id = item["id"]

    # 2. Sign-off / Verify claim
    res_sign = client.post(
        f"/api/v1/verification/queue/{queue_id}/sign-off",
        json={
            "approved": True,
            "notes": "Verified against German Commercial Register HRB 4821 and REACH chemical lab certificates.",
            "reviewer": "Trade OS Senior Auditor"
        },
        headers=AUTH_HEADERS
    )
    assert res_sign.status_code == 200
    signed = res_sign.json()
    assert signed["status"] == "verified"
    assert "Trade OS Senior Auditor" in signed["assigned_to"]

def test_data_corrections():
    # Submit data correction
    fake_entity_id = str(uuid.uuid4())
    res_corr = client.post(
        "/api/v1/verification/corrections",
        json={
            "entity_id": fake_entity_id,
            "entity_type": "company",
            "field_name": "vat_number",
            "old_value": "DE123456789",
            "new_value": "DE987654321",
            "reason": "VAT registration changed after GmbH restructuring",
            "reporter_email": "compliance@butlers.in"
        },
        headers=AUTH_HEADERS
    )
    assert res_corr.status_code == 200
    corr = res_corr.json()
    assert corr["status"] == "submitted"
    assert corr["new_value"] == "DE987654321"

def test_entity_resolution():
    # 1. List resolution links
    res_links = client.get("/api/v1/verification/entity-resolution", headers=AUTH_HEADERS)
    assert res_links.status_code == 200
    assert isinstance(res_links.json(), list)
