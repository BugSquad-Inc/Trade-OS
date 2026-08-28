from sqlalchemy.orm import Session
from app.repositories import account_repo, capability_repo, match_repo, signal_repo
from app.services import scoring_service, lane_service, compliance_service

def execute_nightly_pipeline(db: Session) -> dict:
    """Nightly batch pipeline: recalculates match scores, updates signals, logs append-only history."""
    exporter = capability_repo.get_exporter_capability(db)
    buyers = account_repo.get_all_buyers(db)

    scored_count = 0
    for idx, buyer in enumerate(buyers, start=1):
        score = scoring_service.score_match(buyer, exporter, rank=min(idx, 5))
        
        match_repo.upsert_match_candidate(db, {
            "buyer_id": buyer.id,
            "total_score": score.total_score,
            "product_fit_score": score.product_fit_score,
            "compliance_score": score.compliance_score,
            "lane_economics_score": score.lane_economics_score,
            "intent_signals_score": score.intent_signals_score,
            "accessibility_score": score.accessibility_score,
            "grade": score.grade,
            "rank": idx,
            "score_version": "v1.0.0",
            "drivers": [d.model_dump() for d in score.drivers],
            "key_gaps": score.key_gaps,
            "next_best_action": score.next_best_action,
            "outreach_angle": score.outreach_angle,
            "status": "suggested"
        })

        # History: INSERT ONLY (Rule 7)
        match_repo.insert_score_history(
            db,
            buyer_id=buyer.id,
            score=score.total_score,
            score_version="v1.0.0",
            drivers=[d.model_dump() for d in score.drivers]
        )
        scored_count += 1

    return {
        "buyers_scored": scored_count,
        "signals_emitted": signal_repo.get_signals(db, limit=500).__len__()
    }

if __name__ == "__main__":
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        res = execute_nightly_pipeline(db)
        print(f"[NIGHTLY REFRESH WORKER COMPLETE] {res}")
    finally:
        db.close()
