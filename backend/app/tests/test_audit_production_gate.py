import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": "tradeos_pilot_secret_key_2026"}

def test_centralized_audit_trail():
    # 1. Fetch Audit Events
    res = client.get("/api/v1/audit/events", headers=AUTH_HEADERS)
    assert res.status_code == 200
    events = res.json()
    assert len(events) >= 4
    categories = [e["event_category"] for e in events]
    assert "COMPLIANCE_SIGN_OFF" in categories
    assert "FINANCE_MODIFICATION" in categories

    # 2. Log a new audit event
    res_log = client.post(
        "/api/v1/audit/events",
        json={
            "event_category": "ACCESS",
            "action": "EXPORT_DOSSIER_DOWNLOAD",
            "entity_type": "entity_company",
            "actor_email": "johann@butlers.in",
            "ip_address": "49.207.182.90",
            "user_agent": "TradeOS-Client/2.0",
            "payload_diff": {"target_buyer": "Picard GmbH", "format": "PDF"}
        },
        headers=AUTH_HEADERS
    )
    assert res_log.status_code == 200
    logged = res_log.json()
    assert logged["action"] == "EXPORT_DOSSIER_DOWNLOAD"
    assert logged["event_category"] == "ACCESS"

    # 3. Audit Stats
    res_stats = client.get("/api/v1/audit/stats", headers=AUTH_HEADERS)
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["total_audit_events"] >= 5
    assert stats["tamper_evident_status"] == "GUARANTEED_INSERT_ONLY"

def test_production_secure_mvp_gate():
    """Final MVP Production Gate validating end-to-end operational readiness."""
    # 1. Health Endpoints
    assert client.get("/api/v1/health/live").status_code == 200
    assert client.get("/api/v1/health/ready").status_code == 200

    # 2. Tenancy & RBAC
    res_tenant = client.get("/api/v1/tenants/current", headers=AUTH_HEADERS)
    assert res_tenant.status_code == 200
    assert res_tenant.json()["country_code"] == "IN"

    # 3. Today Cockpit
    res_today = client.get("/api/v1/today", headers=AUTH_HEADERS)
    assert res_today.status_code == 200
    assert res_today.json()["exporter_name"] != ""

    # 4. Deals & Landed Cost Engine
    res_calc = client.post(
        "/api/v1/deals/calculator/landed-cost",
        json={
            "unit_price_inr": 280.0,
            "quantity_sqft": 10000,
            "freight_usd": 1850.0,
            "customs_duty_pct": 0.0,
            "target_margin_pct": 25.0
        },
        headers=AUTH_HEADERS
    )
    assert res_calc.status_code == 200
    calc = res_calc.json()
    assert calc["recommended_unit_price_eur"] > 3.0

    # 5. Compliance Rule Engine v2
    res_audit = client.post(
        "/api/v1/documents/compliance-audit",
        json={
            "exporter_certs": ["LWG Gold Rated", "ISO 14001:2015"],
            "has_farm_polygons": True,
            "cr_vi_tested_zero": True,
            "reach_svhc_zero": True
        },
        headers=AUTH_HEADERS
    )
    assert res_audit.status_code == 200
    assert res_audit.json()["overall_score"] >= 90
