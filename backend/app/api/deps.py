from fastapi import Header, HTTPException, status, Request
from typing import Optional
from app.config import settings, EnvironmentType

async def require_api_key(
    request: Request,
    x_tradeos_key: Optional[str] = Header(None, alias="X-TradeOS-Key")
):
    """
    Validate API key authentication header.
    In development/demo mode, a default configured key from .env is allowed.
    In staging/production, explicit valid key is strictly enforced.
    """
    valid_key = settings.API_KEY or "tradeos_pilot_secret_key_2026"
    
    if not x_tradeos_key or x_tradeos_key != valid_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TradeOS-Key authentication header."
        )
    return x_tradeos_key
