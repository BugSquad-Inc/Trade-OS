from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

def execute_keyword_search(db: Session, query: str, country_code: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    """Sparse BM25 / Trigram full-text search over silver.entity_company."""
    params = {"query": query, "limit": limit}
    where_clauses = [
        """(
            to_tsvector('english', coalesce(canonical_name, '') || ' ' || coalesce(segment, '') || ' ' || coalesce(description, '')) @@ plainto_tsquery('english', :query)
            OR canonical_name ILIKE '%' || :query || '%'
            OR segment ILIKE '%' || :query || '%'
            OR description ILIKE '%' || :query || '%'
        )"""
    ]
    if country_code:
        where_clauses.append("country_code = :country")
        params["country"] = country_code

    where_sql = " AND ".join(where_clauses)
    sql = f"""
        SELECT 
            id, canonical_name, country_code, city, segment, description,
            ts_rank_cd(to_tsvector('english', coalesce(canonical_name, '') || ' ' || coalesce(segment, '') || ' ' || coalesce(description, '')), plainto_tsquery('english', :query)) as rank_score,
            similarity(canonical_name, :query) as trigram_score
        FROM silver.entity_company
        WHERE {where_sql}
        ORDER BY rank_score DESC, trigram_score DESC
        LIMIT :limit
    """
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
