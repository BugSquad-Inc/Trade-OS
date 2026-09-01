from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.repositories import match_repo, capability_repo
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
        
        # Calculate dynamic match score using v2.0 engine
        match_eval = scoring_service.score_match(buyer=buyer, exporter=exporter, rank=c.rank)

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
            "total_score": match_eval.total_score,
            "grade": match_eval.grade,
            "score_version": match_eval.score_version,
            "is_compliance_gate_failed": match_eval.is_compliance_gate_failed,
            "compliance_gate_reason": match_eval.compliance_gate_reason,
            "score_breakdown": {
                "product_fit": match_eval.product_fit_score,
                "compliance": match_eval.compliance_score,
                "lane_economics": match_eval.lane_economics_score,
                "intent_signals": match_eval.intent_signals_score,
                "accessibility": match_eval.accessibility_score
            },
            "drivers": [d.model_dump() for d in match_eval.drivers],
            "counter_factuals": [cf.model_dump() for cf in match_eval.counter_factuals],
            "key_gaps": match_eval.key_gaps,
            "next_best_action": match_eval.next_best_action,
            "outreach_angle": match_eval.outreach_angle,
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
