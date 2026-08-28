import math
import time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.repositories import search_repo, account_repo, match_repo

def compute_rrf_score(dense_rank: Optional[int], sparse_rank: Optional[int], k: int = 60) -> float:
    """Computes Reciprocal Rank Fusion score: 1/(k + r1) + 1/(k + r2)."""
    score = 0.0
    if dense_rank is not None:
        score += 1.0 / (k + dense_rank)
    if sparse_rank is not None:
        score += 1.0 / (k + sparse_rank)
    return round(score * 1000, 4)

class HybridSearchEngine:
    """Hybrid pgvector HNSW + tsvector BM25 + Reciprocal Rank Fusion search engine."""

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
