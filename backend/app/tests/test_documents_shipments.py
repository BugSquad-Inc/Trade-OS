import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": "tradeos_pilot_secret_key_2026"}

def test_documents_vault_and_audit():
    # 1. List Documents
    res = client.get("/api/v1/documents", headers=AUTH_HEADERS)
    assert res.status_code == 200
    docs = res.json()
    assert len(docs) >= 3
    doc_types = [d["doc_type"] for d in docs]
    assert "eudr_dds" in doc_types
    assert "lab_test_report" in doc_types

    # 2. Run Compliance Rule Engine v2
    res_audit = client.post(
        "/api/v1/documents/compliance-audit",
        json={
            "exporter_certs": ["LWG Gold Rated", "ISO 14001:2015", "REACH SVHC Tested"],
            "has_farm_polygons": True,
            "cr_vi_tested_zero": True,
            "reach_svhc_zero": True
        },
        headers=AUTH_HEADERS
    )
    assert res_audit.status_code == 200
    audit = res_audit.json()
    assert audit["overall_score"] >= 90
    assert "Grade A" in audit["clearance_grade"]
    assert len(audit["checks"]) >= 5

def test_shipments_and_ebrc_tracking():
    # 1. List Shipments
    res = client.get("/api/v1/shipments", headers=AUTH_HEADERS)
    assert res.status_code == 200
    shipments = res.json()
    assert len(shipments) >= 2

    first_shipment = shipments[0]
    assert "container_number" in first_shipment
    assert "milestone" in first_shipment
    assert "ebrc_status" in first_shipment
    shipment_id = first_shipment["id"]

    # 2. Update Milestone & eBRC
    res_up = client.patch(
        f"/api/v1/shipments/{shipment_id}/milestone",
        json={
            "milestone": "vessel_arrived",
            "tracking_status": "on_time",
            "ebrc_status": "applied",
            "realized_amount_inr": 4162500.0
        },
        headers=AUTH_HEADERS
    )
    assert res_up.status_code == 200
    updated = res_up.json()
    assert updated["milestone"] == "vessel_arrived"
    assert updated["ebrc_status"] == "applied"
    assert updated["realized_amount_inr"] == 4162500.0
