import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/tests/test_scoring.py
w("backend/app/tests/test_scoring.py", """import pytest
from app.services.scoring_service import score_match, grade_from_score

class DummyCompany:
    canonical_name = "Picard GmbH"
    segment = "Leather goods"

class DummyExporter:
    company_name = "Butler's Leather"
    eudr_readiness_score = 68

def test_grade_boundaries():
    assert grade_from_score(90.0) == "A"
    assert grade_from_score(85.0) == "A"
    assert grade_from_score(84.9) == "B"
    assert grade_from_score(70.0) == "B"
    assert grade_from_score(55.0) == "C"
    assert grade_from_score(50.0) == "D"

def test_score_match_structure():
    score = score_match(DummyCompany(), DummyExporter(), rank=1)
    assert score.total_score == 88.0
    assert score.grade == "A"
    assert len(score.drivers) == 5
    assert score.product_fit_score == 32.0
    assert score.compliance_score == 22.0
    assert score.lane_economics_score == 13.5
    assert score.intent_signals_score == 13.0
    assert score.accessibility_score == 7.5
    assert len(score.key_gaps) > 0
    assert score.next_best_action is not None
""")

# 2. backend/app/tests/test_capability.py
w("backend/app/tests/test_capability.py", """import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_capability_unauthorized():
    response = client.get("/api/v1/capability")
    assert response.status_code == 401

def test_capability_authorized():
    response = client.get("/api/v1/capability", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Butler's Leather"
    assert data["eudr_readiness_score"] == 68
    assert "LWG Gold Rated" in str(data["certifications"])
    assert "Chennai Port (INMAA)" in data["port_of_export"]
""")

# 3. backend/app/tests/test_matches.py
w("backend/app/tests/test_matches.py", """import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_matches_unauthorized():
    response = client.get("/api/v1/matches")
    assert response.status_code == 401

def test_matches_authorized():
    response = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] == 5
    assert len(data["matches"]) == 5

    top_match = data["matches"][0]
    assert top_match["rank"] == 1
    assert top_match["name"] == "Picard GmbH"
    assert top_match["grade"] == "A"
    assert top_match["total_score"] >= 85.0
    assert len(top_match["drivers"]) == 5
    assert top_match["contact"]["verification_status"] == "verified"
""")

# 4. backend/app/tests/test_signals.py
w("backend/app/tests/test_signals.py", """import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_signals_endpoint():
    response = client.get("/api/v1/signals", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["total_count"] >= 5
    assert "eudr_scorecard" in data
    assert data["eudr_scorecard"]["readiness_score"] == 68
    assert "freight_benchmark" in data
    assert data["freight_benchmark"]["rate_usd"] == 1850.0
""")

# 5. backend/app/tests/test_accounts.py
w("backend/app/tests/test_accounts.py", """import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_account_360_detail():
    # First get matches to find Picard GmbH id
    m_res = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    picard = m_res.json()["matches"][0]
    buyer_id = picard["buyer_id"]

    response = client.get(f"/api/v1/accounts/{buyer_id}", headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["canonical_name"] == "Picard GmbH"
    assert data["country"] == "Germany"
    assert len(data["contacts"]) >= 1
    contact = data["contacts"][0]
    assert contact["legal_basis"] == "B2B legitimate interest under GDPR Art. 6(1)(f)"
    assert contact["confidence"] >= 0.8
    assert len(data["eudr_requirements"]) >= 4
    assert "lane_economics" in data
""")

# 6. backend/app/tests/test_outreach.py
w("backend/app/tests/test_outreach.py", """import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)

def test_outreach_generation():
    m_res = client.get("/api/v1/matches", headers={"X-TradeOS-Key": settings.API_KEY})
    picard = m_res.json()["matches"][0]
    buyer_id = picard["buyer_id"]

    payload = {
        "buyer_id": buyer_id,
        "tone": "Professional"
    }

    response = client.post("/api/v1/outreach", json=payload, headers={"X-TradeOS-Key": settings.API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert data["buyer_name"] == "Picard GmbH"
    assert data["tone"] == "Professional"
    assert "EUDR" in data["subject"]
    assert "Butler's Leather" in data["body"]
    assert "Chennai" in data["body"]
""")

print("[SUCCESS] Part 7 (Test Suite) built successfully")
