import uuid
from fastapi import Header, HTTPException, status, Request, Depends
from typing import Optional, List
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.tenant import Tenant, UserAccount, UserRole

async def require_api_key(
    request: Request,
    x_tradeos_key: Optional[str] = Header(None, alias="X-TradeOS-Key")
):
    """
    Validate API key authentication header.
    """
    valid_key = settings.API_KEY or "tradeos_pilot_secret_key_2026"
    
    if not x_tradeos_key or x_tradeos_key != valid_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TradeOS-Key authentication header."
        )
    return x_tradeos_key

async def get_current_tenant(
    x_tenant_id: Optional[str] = Header(None, alias="X-Tenant-ID"),
    db: Session = Depends(get_db)
) -> Tenant:
    """Resolve current tenant context from header or return default primary tenant."""
    if x_tenant_id:
        try:
            t_uuid = uuid.UUID(x_tenant_id)
            tenant = db.query(Tenant).filter(Tenant.id == t_uuid).first()
            if tenant:
                return tenant
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified tenant not found.")
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid X-Tenant-ID format.")
    
    # Default to primary pilot tenant (Butler's Leather)
    tenant = db.query(Tenant).first()
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active tenant found.")
    return tenant

def require_role(allowed_roles: List[UserRole]):
    """
    Dependency factory enforcing role-based access control (RBAC).
    Returns 403 Forbidden if user role is not permitted.
    """
    def role_checker(
        x_user_role: Optional[str] = Header(None, alias="X-User-Role"),
        x_user_id: Optional[str] = Header(None, alias="X-User-ID"),
        db: Session = Depends(get_db)
    ):
        current_role: Optional[UserRole] = None

        if x_user_id:
            try:
                u_uuid = uuid.UUID(x_user_id)
                user = db.query(UserAccount).filter(UserAccount.id == u_uuid).first()
                if user:
                    current_role = user.role
            except ValueError:
                pass

        if not current_role and x_user_role:
            try:
                current_role = UserRole(x_user_role)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid X-User-Role '{x_user_role}'. Valid roles: {[r.value for r in UserRole]}"
                )

        # Default to 'owner' if no role header provided in dev
        if not current_role:
            current_role = UserRole.owner

        # Admin and owner have universal super-access
        if current_role in (UserRole.admin, UserRole.owner):
            return current_role

        if current_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: User role '{current_role.value}' is not authorized. Required: {[r.value for r in allowed_roles]}"
            )
        return current_role

    return role_checker
