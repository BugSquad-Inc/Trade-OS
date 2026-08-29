import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.tenant import (
    TenantResponse,
    UserAccountResponse,
    InviteMemberRequest,
    UpdateRoleRequest
)
from app.repositories import tenant_repo

router = APIRouter(prefix="/api/v1/tenants", tags=["Multi-Tenancy & RBAC"], dependencies=[Depends(require_api_key)])

@router.get("/current", response_model=TenantResponse)
def get_current_tenant(db: Session = Depends(get_db)):
    """Retrieve details, subscription plan, and team members of the active tenant organization."""
    tenant = tenant_repo.get_default_tenant(db)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant organisation not found.")
    return tenant

@router.get("/members", response_model=List[UserAccountResponse])
def list_team_members(db: Session = Depends(get_db)):
    """List all authorized team members in the current organization."""
    tenant = tenant_repo.get_default_tenant(db)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant organisation not found.")
    return tenant_repo.list_tenant_members(db, tenant_id=tenant.id)

@router.post("/members/invite", response_model=UserAccountResponse)
def invite_team_member(invite_in: InviteMemberRequest, db: Session = Depends(get_db)):
    """Invite and provision a new user with specific role permissions (owner, sales, compliance, finance, auditor)."""
    tenant = tenant_repo.get_default_tenant(db)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant organisation not found.")
    return tenant_repo.invite_member(db, tenant_id=tenant.id, data=invite_in.model_dump())

@router.patch("/members/{user_id}/role", response_model=UserAccountResponse)
def change_user_role(user_id: uuid.UUID, role_in: UpdateRoleRequest, db: Session = Depends(get_db)):
    """Update role-based access control level for a team member."""
    user = tenant_repo.update_member_role(db, user_id=user_id, new_role=role_in.role)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user
