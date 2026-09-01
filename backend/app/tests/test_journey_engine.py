import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": settings.API_KEY}

def test_journey_golden_path_and_governance():
    # 1. Fetch existing deals or create one
    deals_res = client.get("/api/v1/deals", headers=AUTH_HEADERS)
    assert deals_res.status_code == 200
    deals = deals_res.json()
    assert len(deals) > 0
    opp_id = deals[0]["id"]

    # 2. Query journey state
    state_res = client.get(f"/api/v1/journey/opportunities/{opp_id}/state", headers=AUTH_HEADERS)
    assert state_res.status_code == 200
    state = state_res.json()
    assert "current_stage" in state
    assert "macro_stage" in state
    assert "available_actions" in state
    assert "owner_question" in state
    assert len(state["available_actions"]) > 0

    # 3. Test Invalid Transition Rejection (Cannot jump to closed_won directly from initial stages)
    invalid_req = {
        "action_id": "complete_order",
        "actor": "Johann Butler",
        "actor_role": "owner",
        "reason_code": "invalid_jump"
    }
    invalid_res = client.post(f"/api/v1/journey/opportunities/{opp_id}/transition", json=invalid_req, headers=AUTH_HEADERS)
    assert invalid_res.status_code == 400
    assert "Transition rejected" in invalid_res.json()["detail"]

    # 4. Test Valid Next Action Execution
    first_action = state["available_actions"][0]
    idempotency_key = f"test-idem-{uuid.uuid4().hex[:8]}"
    valid_req = {
        "action_id": first_action["action_id"],
        "actor": "Johann Butler",
        "actor_role": "owner",
        "reason_code": "owner_decision",
        "notes": "Transition executed via Journey Engine test",
        "idempotency_key": idempotency_key
    }
    trans_res = client.post(f"/api/v1/journey/opportunities/{opp_id}/transition", json=valid_req, headers=AUTH_HEADERS)
    assert trans_res.status_code == 200
    trans_data = trans_res.json()
    assert trans_data["success"] is True
    assert "event_id" in trans_data
    assert trans_data["new_stage"] == first_action["target_stage"]

    # 5. Test Idempotency (Repeat with same idempotency_key)
    repeat_res = client.post(f"/api/v1/journey/opportunities/{opp_id}/transition", json=valid_req, headers=AUTH_HEADERS)
    assert repeat_res.status_code == 200
    assert repeat_res.json()["event_id"] == trans_data["event_id"]

    # 6. Verify Immutable History
    hist_res = client.get(f"/api/v1/journey/opportunities/{opp_id}/history", headers=AUTH_HEADERS)
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) >= 1
    assert any(h["id"] == trans_data["event_id"] for h in history)
