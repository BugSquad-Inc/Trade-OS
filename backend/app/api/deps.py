from fastapi import Header, HTTPException, status
from typing import Optional
from app.config import settings

async def require_api_key(x_tradeos_key: Optional[str] = Header(None, alias="X-TradeOS-Key")):
    if not x_tradeos_key or x_tradeos_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-TradeOS-Key authentication header."
        )
    return x_tradeos_key
