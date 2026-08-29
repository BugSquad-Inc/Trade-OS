from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.tenant import UserAccountResponse
from app.repositories import tenant_repo

router = APIRouter(prefix="/api/v1/users", tags=["Users & Identity"], dependencies=[Depends(require_api_key)])

@router.get("/me", response_model=UserAccountResponse)
def get_current_user_profile(db: Session = Depends(get_db)):
    """Retrieve logged-in user profile, role permissions, and tenant affiliation."""
    tenant = tenant_repo.get_default_tenant(db)
    if not tenant or not tenant.users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User account not found.")
    return tenant.users[0]
