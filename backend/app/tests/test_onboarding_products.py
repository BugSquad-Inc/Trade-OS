import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": "tradeos_pilot_secret_key_2026"}

def test_exporter_profile_and_readiness():
    # 1. Get Exporter Profile
    res = client.get("/api/v1/exporters/profile", headers=AUTH_HEADERS)
    assert res.status_code == 200
    profile = res.json()
    assert profile["company_name"] == "Butler's Leather"
    assert "pan" in profile
    assert "gstin_list" in profile
    assert "ad_code" in profile
    assert "onboarding_step" in profile

    # 2. Update Profile Partial
    res_update = client.patch(
        "/api/v1/exporters/profile",
        json={"location": "Chennai / Ambur, Tamil Nadu, India", "monthly_capacity_sqft": 55000},
        headers=AUTH_HEADERS
    )
    assert res_update.status_code == 200
    assert res_update.json()["location"] == "Chennai / Ambur, Tamil Nadu, India"
    assert res_update.json()["monthly_capacity_sqft"] == 55000

    # 3. Save-and-resume Onboarding Step
    res_step = client.post(
        "/api/v1/exporters/onboarding/step",
        json={"step": 3, "data": {"facilities": [{"name": "Unit 1", "workers": 90}]}},
        headers=AUTH_HEADERS
    )
    assert res_step.status_code == 200
    assert res_step.json()["onboarding_step"] >= 3

    # 4. Readiness Gaps Analysis
    res_gaps = client.get("/api/v1/exporters/readiness-gaps", headers=AUTH_HEADERS)
    assert res_gaps.status_code == 200
    gaps = res_gaps.json()
    assert "overall_score" in gaps
    assert "mandatory_checks" in gaps
    assert "recommended_checks" in gaps

def test_product_passports_and_versions():
    # 1. List Products
    res = client.get("/api/v1/products", headers=AUTH_HEADERS)
    assert res.status_code == 200
    products = res.json()
    assert len(products) >= 3
    
    first_prod = products[0]
    assert "hs_code" in first_prod
    assert len(first_prod["versions"]) >= 1
    
    # Check that seeded products carry certificates and passports
    all_certs = [c for p in products for v in p["versions"] for c in v["certificates"]]
    all_passports = [passp for p in products for v in p["versions"] for passp in v["passports"]]
    assert len(all_certs) >= 1
    assert len(all_passports) >= 1

    # 2. Get Passport for Version
    version_with_pass = next(v for p in products for v in p["versions"] if len(v.get("passports", [])) > 0)
    version_id = version_with_pass["id"]
    res_pass = client.get(f"/api/v1/products/versions/{version_id}/passport", headers=AUTH_HEADERS)
    assert res_pass.status_code == 200
    passport = res_pass.json()
    assert "passport_number" in passport
    assert "passport_metadata" in passport

    # 3. Create a New Product Family
    res_create = client.post(
        "/api/v1/products",
        json={
            "name": "Vegetable Tanned Buffalo Crust for Belts",
            "category": "Finished Buffalo Leather",
            "hs_code": "4104",
            "itc_hs_code": "4104.41.00",
            "leather_type": "Buffalo Crust",
            "description": "Heavy temper buffalo crust for equestrian and heavy duty belts",
            "materials": ["Buffalo Rawhide", "Mimosa Tanning Extracts"],
            "finishes": ["Natural drum dyed"],
            "thickness_range_mm": ["2.8-3.4"],
            "monthly_capacity_sqft": 12000,
            "moq_sqft": 1000,
            "price_basis_inr": 310.0,
            "price_basis_usd": 3.70
        },
        headers=AUTH_HEADERS
    )
    assert res_create.status_code == 200
    created = res_create.json()
    assert created["name"] == "Vegetable Tanned Buffalo Crust for Belts"
    assert len(created["versions"]) == 1
    assert len(created["versions"][0]["passports"]) == 1
