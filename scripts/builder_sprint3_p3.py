import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/tests/test_hybrid_search.py
w("backend/app/tests/test_hybrid_search.py", """import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.services.search_service import compute_rrf_score

client = TestClient(app)

def test_rrf_math():
    score_top1 = compute_rrf_score(1, 1, k=60)
    score_dense_only = compute_rrf_score(1, None, k=60)
    score_sparse_only = compute_rrf_score(None, 1, k=60)
    
    assert score_top1 > score_dense_only
    assert score_top1 > score_sparse_only
    assert score_dense_only == score_sparse_only

def test_hybrid_search_endpoint():
    payload = {
        "query": "luxury leather handbag",
        "top_k": 5
    }
    response = client.post("/api/v1/search/hybrid", json=payload, headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "luxury leather handbag"
    assert data["total_results"] > 0
    assert len(data["results"]) <= 5
    top_hit = data["results"][0]
    assert "rrf_score" in top_hit
    assert "relevance_explanation" in top_hit
""")

# 2. backend/app/tests/test_agents.py
w("backend/app/tests/test_agents.py", """import pytest
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
""")

print("[SUCCESS] Sprint 3 Part 3 (Pytest suite for M10 & M11) built successfully")
