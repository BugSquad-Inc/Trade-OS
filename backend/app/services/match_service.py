from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.repositories import match_repo, account_repo, capability_repo
from app.services import scoring_service, lane_service, compliance_service

def list_ranked_matches(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    candidates = match_repo.get_match_candidates(db, limit=limit)
    exporter = capability_repo.get_exporter_capability(db)
    lane = lane_service.get_active_lane_benchmark(db)
    eudr = compliance_service.calculate_eudr_readiness(exporter)

    result = []
    for c in candidates:
        buyer = c.company
        primary_contact = next((p for p in buyer.persons if p.is_primary), buyer.persons[0] if buyer.persons else None)

        result.append({
            "id": str(c.id),
            "buyer_id": str(c.buyer_id),
            "name": buyer.canonical_name,
            "legal_name": buyer.legal_name or buyer.canonical_name,
            "country_code": buyer.country_code,
            "country": "Germany" if buyer.country_code == "DE" else buyer.country_code,
            "city": buyer.city or "Germany",
            "segment": buyer.segment,
            "rank": c.rank,
            "total_score": float(c.total_score),
            "grade": c.grade,
            "score_breakdown": {
                "product_fit": float(c.product_fit_score),
                "compliance": float(c.compliance_score),
                "lane_economics": float(c.lane_economics_score),
                "intent_signals": float(c.intent_signals_score),
                "accessibility": float(c.accessibility_score)
            },
            "drivers": c.drivers,
            "key_gaps": c.key_gaps,
            "next_best_action": c.next_best_action,
            "outreach_angle": c.outreach_angle,
            "status": c.status,
            "contact": {
                "full_name": primary_contact.full_name if primary_contact else "Head of Procurement",
                "title": primary_contact.title if primary_contact else "Procurement Lead",
                "email": primary_contact.email if primary_contact else None,
                "confidence": float(primary_contact.confidence) if primary_contact else 0.8,
                "verification_status": primary_contact.verification_status if primary_contact else "illustrative"
            } if primary_contact else None,
            "freight_summary": f"Chennai → Hamburg: {lane['transit_days']} (${lane['rate_usd']:,.0f}/FEU)",
            "eudr_readiness_score": eudr["readiness_score"]
        })
    return result
