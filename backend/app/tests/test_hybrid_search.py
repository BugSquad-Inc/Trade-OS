import pytest
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
