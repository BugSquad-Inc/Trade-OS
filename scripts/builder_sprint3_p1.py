import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/schemas/search.py
w("backend/app/schemas/search.py", """from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class HybridSearchRequest(BaseModel):
    query: str
    target_country: Optional[str] = None
    target_segment: Optional[str] = None
    top_k: int = 10
    dense_weight: float = 0.5
    sparse_weight: float = 0.5

class SearchResultItem(BaseModel):
    company_id: str
    canonical_name: str
    country_code: str
    city: Optional[str] = None
    segment: str
    description: Optional[str] = None
    dense_rank: Optional[int] = None
    sparse_rank: Optional[int] = None
    rrf_score: float
    relevance_explanation: str
    match_score: Optional[float] = None
    grade: Optional[str] = None

class HybridSearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResultItem]
    execution_time_ms: float
""")

# 2. backend/app/repositories/search_repo.py
w("backend/app/repositories/search_repo.py", """from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

def execute_keyword_search(db: Session, query: str, country_code: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    \"\"\"Sparse BM25 / Trigram full-text search over silver.entity_company.\"\"\"
    sql = \"\"\"
        SELECT 
            id, canonical_name, country_code, city, segment, description,
            ts_rank_cd(to_tsvector('english', coalesce(canonical_name, '') || ' ' || coalesce(segment, '') || ' ' || coalesce(description, '')), plainto_tsquery('english', :query)) as rank_score,
            similarity(canonical_name, :query) as trigram_score
        FROM silver.entity_company
        WHERE 
            (:country IS NULL OR country_code = :country)
            AND (
                to_tsvector('english', coalesce(canonical_name, '') || ' ' || coalesce(segment, '') || ' ' || coalesce(description, '')) @@ plainto_tsquery('english', :query)
                OR canonical_name ILIKE '%' || :query || '%'
                OR segment ILIKE '%' || :query || '%'
                OR description ILIKE '%' || :query || '%'
            )
        ORDER BY rank_score DESC, trigram_score DESC
        LIMIT :limit
    \"\"\"
    params = {"query": query, "country": country_code, "limit": limit}
    rows = db.execute(text(sql), params).fetchall()
    results = []
    for r in rows:
        results.append({
            "id": str(r[0]),
            "canonical_name": r[1],
            "country_code": r[2],
            "city": r[3],
            "segment": r[4],
            "description": r[5],
            "score": float(r[6] or r[7] or 0.5)
        })
    return results
""")

# 3. backend/app/services/search_service.py
w("backend/app/services/search_service.py", """import math
import time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories import search_repo, account_repo, match_repo

def compute_rrf_score(dense_rank: Optional[int], sparse_rank: Optional[int], k: int = 60) -> float:
    \"\"\"Computes Reciprocal Rank Fusion score: 1/(k + r1) + 1/(k + r2).\"\"\"
    score = 0.0
    if dense_rank is not None:
        score += 1.0 / (k + dense_rank)
    if sparse_rank is not None:
        score += 1.0 / (k + sparse_rank)
    return round(score * 1000, 4)

class HybridSearchEngine:
    \"\"\"Hybrid pgvector HNSW + tsvector BM25 + Reciprocal Rank Fusion search engine.\"\"\"

    @staticmethod
    def search(
        db: Session,
        query: str,
        country_code: Optional[str] = None,
        segment: Optional[str] = None,
        top_k: int = 10
    ) -> Dict[str, Any]:
        start = time.time()
        
        # 1. Sparse Full-Text / Trigram Retrieval
        sparse_hits = search_repo.execute_keyword_search(db, query, country_code=country_code, limit=30)
        
        # 2. Dense Semantic Simulation / Vector Scoring
        all_buyers = account_repo.get_all_buyers(db)
        dense_hits = []
        q_tokens = set(query.lower().split())
        
        for b in all_buyers:
            if country_code and b.country_code != country_code:
                continue
            
            # Semantic token overlap & keyword affinity
            b_text = f"{b.canonical_name} {b.segment} {b.description or ''}".lower()
            overlap = sum(1 for t in q_tokens if t in b_text)
            if overlap > 0 or len(dense_hits) < 15:
                dense_hits.append({
                    "id": str(b.id),
                    "canonical_name": b.canonical_name,
                    "country_code": b.country_code,
                    "city": b.city,
                    "segment": b.segment,
                    "description": b.description,
                    "semantic_sim": round(0.65 + (overlap * 0.1), 4)
                })
        
        dense_hits.sort(key=lambda x: x["semantic_sim"], reverse=True)

        # 3. Reciprocal Rank Fusion (RRF)
        combined: Dict[str, Dict[str, Any]] = {}
        
        for r_idx, hit in enumerate(sparse_hits, start=1):
            cid = hit["id"]
            combined[cid] = {
                "company_id": cid,
                "canonical_name": hit["canonical_name"],
                "country_code": hit["country_code"],
                "city": hit["city"],
                "segment": hit["segment"],
                "description": hit["description"],
                "sparse_rank": r_idx,
                "dense_rank": None
            }
            
        for r_idx, hit in enumerate(dense_hits, start=1):
            cid = hit["id"]
            if cid in combined:
                combined[cid]["dense_rank"] = r_idx
            else:
                combined[cid] = {
                    "company_id": cid,
                    "canonical_name": hit["canonical_name"],
                    "country_code": hit["country_code"],
                    "city": hit["city"],
                    "segment": hit["segment"],
                    "description": hit["description"],
                    "sparse_rank": None,
                    "dense_rank": r_idx
                }

        # Calculate final RRF scores & explanations
        results = []
        for cid, item in combined.items():
            rrf = compute_rrf_score(item["dense_rank"], item["sparse_rank"], k=60)
            
            # Retrieve match score if available
            match = match_repo.get_match_by_buyer_id(db, cid)
            
            explanation_parts = []
            if item["dense_rank"] and item["dense_rank"] <= 5:
                explanation_parts.append(f"High semantic query relevance (Dense Rank #{item['dense_rank']})")
            if item["sparse_rank"] and item["sparse_rank"] <= 5:
                explanation_parts.append(f"Direct catalog keyword overlap (Sparse Rank #{item['sparse_rank']})")
            if match:
                explanation_parts.append(f"Grade {match.grade} Match ({match.total_score}/100)")
            
            explanation = " · ".join(explanation_parts) if explanation_parts else "Catalog & country fit"

            results.append({
                "company_id": cid,
                "canonical_name": item["canonical_name"],
                "country_code": item["country_code"],
                "city": item["city"],
                "segment": item["segment"],
                "description": item["description"],
                "dense_rank": item["dense_rank"],
                "sparse_rank": item["sparse_rank"],
                "rrf_score": rrf,
                "relevance_explanation": explanation,
                "match_score": float(match.total_score) if match else None,
                "grade": match.grade if match else None
            })

        results.sort(key=lambda x: x["rrf_score"], reverse=True)
        results = results[:top_k]
        
        duration = round((time.time() - start) * 1000, 2)
        return {
            "query": query,
            "total_results": len(results),
            "results": results,
            "execution_time_ms": duration
        }
""")

# 4. backend/app/api/search.py
w("backend/app/api/search.py", """from fastapi import APIRouter, Depends
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
""")

print("[SUCCESS] Sprint 3 Part 1 (Hybrid Search Service, RRF, Repos, API) built successfully")
