import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.tenant import Tenant, UserAccount, TenantMembership, UserRole

def get_default_tenant(db: Session) -> Optional[Tenant]:
    """Retrieve the primary tenant/organisation."""
    stmt = select(Tenant).options(joinedload(Tenant.users), joinedload(Tenant.memberships)).order_by(Tenant.created_at.asc())
    return db.execute(stmt).unique().scalars().first()

def get_tenant_by_id(db: Session, tenant_id: uuid.UUID) -> Optional[Tenant]:
    """Retrieve a tenant by its ID."""
    stmt = select(Tenant).options(joinedload(Tenant.users)).where(Tenant.id == tenant_id)
    return db.execute(stmt).unique().scalar_one_or_none()

def list_tenant_members(db: Session, tenant_id: uuid.UUID) -> List[UserAccount]:
    """List all user accounts belonging to a tenant."""
    stmt = select(UserAccount).where(UserAccount.tenant_id == tenant_id).order_by(UserAccount.created_at.asc())
    return list(db.execute(stmt).scalars().all())

def get_user_by_email(db: Session, email: str) -> Optional[UserAccount]:
    """Retrieve user account by email."""
    stmt = select(UserAccount).where(UserAccount.email == email)
    return db.execute(stmt).scalar_one_or_none()

def invite_member(db: Session, tenant_id: uuid.UUID, data: Dict[str, Any]) -> UserAccount:
    """Invite and provision a new member in the organization with RBAC role."""
    email = data["email"]
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return existing_user

    role = data.get("role", UserRole.sales)
    user = UserAccount(
        tenant_id=tenant_id,
        email=email,
        full_name=data["full_name"],
        role=role,
        is_active=True
    )
    db.add(user)
    db.flush()

    membership = TenantMembership(
        tenant_id=tenant_id,
        user_id=user.id,
        role=role,
        status="active",
        invited_by=data.get("invited_by", "Owner")
    )
    db.add(membership)
    db.commit()
    db.refresh(user)
    return user

def update_member_role(db: Session, user_id: uuid.UUID, new_role: UserRole) -> Optional[UserAccount]:
    """Update a user's RBAC role within the tenant."""
    user = db.execute(select(UserAccount).where(UserAccount.id == user_id)).scalar_one_or_none()
    if not user:
        return None
    user.role = new_role

    membership = db.execute(select(TenantMembership).where(TenantMembership.user_id == user_id)).scalar_one_or_none()
    if membership:
        membership.role = new_role

    db.commit()
    db.refresh(user)
    return user
