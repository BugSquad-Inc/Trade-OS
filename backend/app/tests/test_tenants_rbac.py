import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-TradeOS-Key": "tradeos_pilot_secret_key_2026"}

def test_tenant_and_members():
    # 1. Fetch current tenant
    res = client.get("/api/v1/tenants/current", headers=AUTH_HEADERS)
    assert res.status_code == 200
    tenant = res.json()
    assert "Butler's Leather" in tenant["name"]
    assert tenant["country_code"] == "IN"
    assert len(tenant["users"]) >= 4

    # 2. List members
    res_mem = client.get("/api/v1/tenants/members", headers=AUTH_HEADERS)
    assert res_mem.status_code == 200
    members = res_mem.json()
    assert len(members) >= 4
    roles = [m["role"] for m in members]
    assert "owner" in roles
    assert "sales" in roles
    assert "compliance" in roles
    assert "finance" in roles

    # 3. Invite a new member
    new_email = f"test.logistics.{uuid.uuid4().hex[:4]}@butlers.in"
    res_inv = client.post(
        "/api/v1/tenants/members/invite",
        json={
            "email": new_email,
            "full_name": "Suresh Logistics Manager",
            "role": "finance",
            "invited_by": "Johann Butler"
        },
        headers=AUTH_HEADERS
    )
    assert res_inv.status_code == 200
    invited = res_inv.json()
    assert invited["email"] == new_email
    assert invited["role"] == "finance"

    # 4. Change role to compliance
    user_id = invited["id"]
    res_role = client.patch(
        f"/api/v1/tenants/members/{user_id}/role",
        json={"role": "compliance"},
        headers=AUTH_HEADERS
    )
    assert res_role.status_code == 200
    assert res_role.json()["role"] == "compliance"

def test_current_user_me():
    res_me = client.get("/api/v1/users/me", headers=AUTH_HEADERS)
    assert res_me.status_code == 200
    user = res_me.json()
    assert "email" in user
    assert "role" in user
