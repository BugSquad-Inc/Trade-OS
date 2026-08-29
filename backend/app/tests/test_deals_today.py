import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": "tradeos_pilot_secret_key_2026"}

def test_deals_crud_and_stages():
    # 1. List deals
    res = client.get("/api/v1/deals", headers=AUTH_HEADERS)
    assert res.status_code == 200
    deals = res.json()
    assert len(deals) >= 1
    
    first_deal = deals[0]
    assert "stage" in first_deal
    assert "deal_value_eur" in first_deal
    deal_id = first_deal["id"]

    # 2. Update Stage
    res_stage = client.patch(
        f"/api/v1/deals/{deal_id}/stage",
        json={"stage": "contract_negotiation", "notes": "Contract drafted under standard CISG terms"},
        headers=AUTH_HEADERS
    )
    assert res_stage.status_code == 200
    updated = res_stage.json()
    assert updated["stage"] == "contract_negotiation"

def test_landed_cost_calculator():
    # Test Landed Cost calculation logic
    res_calc = client.post(
        "/api/v1/deals/calculator/landed-cost",
        json={
            "unit_price_inr": 280.0,
            "quantity_sqft": 5000,
            "freight_usd": 1850.0,
            "insurance_usd": 120.0,
            "customs_duty_pct": 0.0,
            "target_margin_pct": 25.0,
            "fx_rate_eur_inr": 92.5
        },
        headers=AUTH_HEADERS
    )
    assert res_calc.status_code == 200
    calc = res_calc.json()
    assert calc["base_eur_per_sqft"] > 3.0
    assert calc["landed_cost_eur_per_sqft"] > 3.0
    assert calc["gross_margin_pct"] >= 20.0
    assert calc["total_quote_value_eur"] > 15000.0

def test_today_cockpit():
    # Fetch Today executive cockpit
    res_today = client.get("/api/v1/today", headers=AUTH_HEADERS)
    assert res_today.status_code == 200
    cockpit = res_today.json()
    assert "exporter_name" in cockpit
    assert "readiness_score" in cockpit
    assert "urgent_tasks" in cockpit
    assert "pipeline_summary" in cockpit
    assert len(cockpit["urgent_tasks"]) >= 1

    # Complete a task
    task_id = cockpit["urgent_tasks"][0]["id"]
    res_comp = client.post(f"/api/v1/today/tasks/{task_id}/complete", headers=AUTH_HEADERS)
    assert res_comp.status_code == 200
    assert res_comp.json()["status"] == "completed"
