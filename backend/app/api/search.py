from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.services.search_service import HybridSearchEngine
from app.schemas.search import HybridSearchRequest, HybridSearchResponse

router = APIRouter(prefix="/api/v1/search", tags=["Hybrid Search"])

@router.post("/hybrid", response_model=HybridSearchResponse)
def hybrid_search(
    req: HybridSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    res = HybridSearchEngine.search(
        db,
        query=req.query,
        country_code=req.target_country,
        segment=req.target_segment,
        top_k=req.top_k
    )
    return HybridSearchResponse(**res)
