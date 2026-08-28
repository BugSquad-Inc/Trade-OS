from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import get_db
from app.api.deps import require_api_key
from app.services import match_service
from app.schemas.match import MatchListResponse

router = APIRouter(prefix="/api/v1", tags=["Matches"])

@router.get("/matches", response_model=MatchListResponse)
def get_matches(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    ranked = match_service.list_ranked_matches(db, limit=limit)
    return MatchListResponse(
        matches=ranked,
        total_count=len(ranked),
        generated_at=datetime.now(timezone.utc).isoformat()
    )
