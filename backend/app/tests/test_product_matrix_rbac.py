import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": settings.API_KEY}

def test_product_matrix_creation_and_dpp():
    # 1. Create a full-spec leather article with physical specs and chemical limits
    article_payload = {
        "name": "Nappa Luxe Automotive Cowhide",
        "category": "Automotive & Luxury Leather",
        "hs_code": "4107",
        "itc_hs_code": "4107.12.00",
        "leather_type": "Bovine Full Grain",
        "description": "Chrome-free soft milled automotive interior crust leather.",
        "materials": ["European Bovine Rawhide", "Synthetic Polymer Tannins"],
        "finishes": ["Semi-Aniline Topcoat", "Hydrophobic Milling"],
        "thickness_range_mm": ["1.1-1.3"],
        "monthly_capacity_sqft": 40000,
        "moq_sqft": 3000,
        "lead_time_days": 25,
        "price_basis_inr": 310.0,
        "price_basis_usd": 3.75,
        "specifications": {
            "thickness_min_mm": 1.1,
            "thickness_max_mm": 1.3,
            "temper": "soft",
            "tensile_strength_n_per_mm2": 18.5,
            "tear_strength_n": 45.0,
            "grain_type": "Full Grain Milled",
            "tannage_type": "Wet-White Chrome Free (FOC)",
            "origin_country": "India"
        },
        "chemical_spec": {
            "chromium_vi_ppm": 0.0,
            "azo_dyes_ppm": 0.0,
            "formaldehyde_ppm": 8.5,
            "pfas_free": True,
            "reach_svhc_status": "compliant",
            "lab_test_report_id": "TR-SGS-2026-9901",
            "accredited_lab": "SGS India / Eurofins"
        },
        "traceability_spec": {
            "abattoir_license_no": "APEDA-TN-8802",
            "mandal_district": "Vaniyambadi / Tirupattur",
            "state": "Tamil Nadu",
            "geolocation_lat": 12.6825,
            "geolocation_lng": 78.6180,
            "eudr_cutoff_cleared": True,
            "hide_origin_batch": "BATCH-2026-AUTO-01"
        }
    }

    res = client.post("/api/v1/products", json=article_payload, headers=AUTH_HEADERS)
    assert res.status_code == 200
    product = res.json()
    assert product["name"] == "Nappa Luxe Automotive Cowhide"
    assert len(product["versions"]) >= 1

    version = product["versions"][0]
    assert version["specifications"]["temper"] == "soft"
    assert version["chemical_spec"]["chromium_vi_ppm"] == 0.0
    assert version["traceability_spec"]["eudr_cutoff_cleared"] is True
    assert len(version["passports"]) >= 1

    passport = version["passports"][0]
    public_token = passport["public_token"]
    assert public_token.startswith("tok_")

    # 2. Test Public unauthenticated DPP endpoint
    public_res = client.get(f"/api/v1/products/dpp/public/{public_token}")
    assert public_res.status_code == 200
    public_dpp = public_res.json()
    assert public_dpp["passport_number"] == passport["passport_number"]
    assert public_dpp["carbon_footprint_kg_co2e"] > 0

def test_rbac_role_enforcement():
    # 1. Test Owner / Compliance role allowed to create versions
    # Fetch existing product
    list_res = client.get("/api/v1/products", headers=AUTH_HEADERS)
    assert list_res.status_code == 200
    products = list_res.json()
    assert len(products) > 0
    fam_id = products[0]["id"]

    version_payload = {
        "version_tag": "v2.0-FOC",
        "materials": ["Bovine Hide"],
        "finishes": ["Matt Wax"],
        "thickness_range_mm": ["1.2-1.4"],
        "monthly_capacity_sqft": 20000,
        "moq_sqft": 2000,
        "lead_time_days": 30,
        "price_basis_inr": 320.0,
        "price_basis_usd": 3.85
    }

    # 2. Logistics role attempting to create version should get 403 Forbidden
    logistics_headers = {**AUTH_HEADERS, "X-User-Role": "logistics"}
    forbidden_res = client.post(f"/api/v1/products/{fam_id}/versions", json=version_payload, headers=logistics_headers)
    assert forbidden_res.status_code == 403
    assert "Access forbidden" in forbidden_res.json()["detail"]

    # 3. Compliance role succeeds
    compliance_headers = {**AUTH_HEADERS, "X-User-Role": "compliance"}
    success_res = client.post(f"/api/v1/products/{fam_id}/versions", json=version_payload, headers=compliance_headers)
    assert success_res.status_code == 200
    assert success_res.json()["version_tag"] == "v2.0-FOC"
