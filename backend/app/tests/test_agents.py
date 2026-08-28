import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_agent_workflow_execution():
    # Retrieve top match buyer id
    m_res = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    buyer = m_res.json()["matches"][0]
    buyer_id = buyer["buyer_id"]

    payload = {
        "buyer_id": buyer_id,
        "requires_human_approval": True
    }
    response = client.post("/api/v1/agents/execute", json=payload, headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["buyer_name"] == buyer["name"]
    assert data["status"] == "completed_pending_approval"
    assert data["approval_required"] is True
    assert len(data["completed_steps"]) == 5

    step_names = [s["agent_name"] for s in data["completed_steps"]]
    assert "ResearchAgent" in step_names
    assert "ComplianceAgent" in step_names
    assert "NarrativeAgent" in step_names
    assert "OutreachSequenceAgent" in step_names
    assert "AccountPlanAgent" in step_names
