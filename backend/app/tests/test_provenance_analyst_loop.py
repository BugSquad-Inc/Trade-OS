import pytest
import uuid
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": settings.API_KEY}

def test_freshness_and_stale_calculation():
    # 1. Fetch companies via matches
    res = client.get("/api/v1/matches", headers=AUTH_HEADERS)
    assert res.status_code == 200
    matches_data = res.json()["matches"]
    assert len(matches_data) > 0
    comp_id = matches_data[0]["buyer_id"]

    # 2. Check freshness endpoint
    fresh_res = client.get(f"/api/v1/verification/freshness/{comp_id}", headers=AUTH_HEADERS)
    assert fresh_res.status_code == 200
    fresh = fresh_res.json()
    assert "is_stale" in fresh
    assert "days_old" in fresh
    assert "freshness_label" in fresh
    assert "effective_truth_status" in fresh

def test_analyst_review_workflow():
    # 1. Fetch queue items
    res_q = client.get("/api/v1/verification/queue", headers=AUTH_HEADERS)
    assert res_q.status_code == 200
    items = res_q.json()
    assert len(items) > 0
    queue_item = items[0]
    queue_id = queue_item["id"]

    # 2. Test Approve Review with Evidence
    review_payload = {
        "decision": "approve",
        "notes": "Verified against German Federal Gazette (Handelsregister) entry HRB-8812.",
        "evidence_reference": "DOC-HRB-2026-DE",
        "reviewer": "Senior Trade OS Research Analyst"
    }
    review_res = client.post(
        f"/api/v1/verification/queue/{queue_id}/review",
        json=review_payload,
        headers={**AUTH_HEADERS, "X-User-Role": "analyst"}
    )
    assert review_res.status_code == 200
    reviewed = review_res.json()
    assert reviewed["status"] == "verified"
    assert "DOC-HRB-2026-DE" in (reviewed["evidence_summary"] or "")
    assert reviewed["assigned_to"] == "Senior Trade OS Research Analyst"

    # 3. Test Dispute Review
    if len(items) > 1:
        dispute_item = items[1]
        dispute_res = client.post(
            f"/api/v1/verification/queue/{dispute_item['id']}/review",
            json={
                "decision": "dispute",
                "notes": "Procurement volume disputed by buyer representative.",
                "evidence_reference": "DISP-REF-9921",
                "reviewer": "Senior Trade OS Research Analyst"
            },
            headers={**AUTH_HEADERS, "X-User-Role": "compliance"}
        )
        assert dispute_res.status_code == 200
        assert dispute_res.json()["status"] == "disputed"
