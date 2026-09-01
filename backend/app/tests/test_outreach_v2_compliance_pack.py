import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": settings.API_KEY}

def test_outreach_modes_and_languages():
    # 1. Fetch valid buyer id from matches
    res_m = client.get("/api/v1/matches", headers=AUTH_HEADERS)
    assert res_m.status_code == 200
    buyer_id = res_m.json()["matches"][0]["buyer_id"]

    # 2. Test German Email (DIN 5008)
    de_email = client.post(
        "/api/v1/outreach",
        json={"buyer_id": buyer_id, "mode": "email", "language": "de", "tone": "Professional"},
        headers=AUTH_HEADERS
    )
    assert de_email.status_code == 200
    de_data = de_email.json()
    assert "Sehr geehrte" in de_data["body"]
    assert "EUDR" in de_data["body"]
    assert len(de_data["why_matches_you"]) > 0
    assert len(de_data["compliance_pack_docs"]) > 0

    # 3. Test WhatsApp Message
    wa_res = client.post(
        "/api/v1/outreach",
        json={"buyer_id": buyer_id, "mode": "whatsapp", "language": "en", "tone": "Direct"},
        headers=AUTH_HEADERS
    )
    assert wa_res.status_code == 200
    wa_data = wa_res.json()
    assert "Digital Passport" in wa_data["body"] or "swatch" in wa_data["body"]
    assert wa_data["mode"] == "whatsapp"

    # 4. Test Cold Calling Phone Script
    phone_res = client.post(
        "/api/v1/outreach",
        json={"buyer_id": buyer_id, "mode": "phone_script", "language": "en", "tone": "Technical"},
        headers=AUTH_HEADERS
    )
    assert phone_res.status_code == 200
    phone_data = phone_res.json()
    assert "GATEKEEPER" in phone_data["body"]
    assert "QUALIFICATION QUESTIONS" in phone_data["body"]
    assert "OBJECTION HANDLING" in phone_data["body"]

def test_compliance_pack_generation():
    res_m = client.get("/api/v1/matches", headers=AUTH_HEADERS)
    buyer_id = res_m.json()["matches"][0]["buyer_id"]

    pack_res = client.get(f"/api/v1/outreach/compliance-pack/{buyer_id}", headers=AUTH_HEADERS)
    assert pack_res.status_code == 200
    pack = pack_res.json()
    assert "bundle_id" in pack
    assert pack["total_documents"] >= 4
    assert any("LWG" in doc["title"] for doc in pack["documents"])
    assert any("TÜV" in doc["title"] for doc in pack["documents"])
    assert any("REACH" in doc["title"] for doc in pack["documents"])
    assert any("EUDR" in doc["title"] for doc in pack["documents"])
