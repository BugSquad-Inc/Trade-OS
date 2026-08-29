import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.tenant import UserRole

class UserAccountResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    oidc_sub: Optional[str] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}

class TenantResponse(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    country_code: str
    plan: str
    status: str
    settings: Dict[str, Any] = Field(default_factory=dict)
    users: List[UserAccountResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class InviteMemberRequest(BaseModel):
    email: str
    full_name: str
    role: UserRole = UserRole.sales
    invited_by: Optional[str] = "Owner"

class UpdateRoleRequest(BaseModel):
    role: UserRole
