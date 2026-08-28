from app.database import SessionLocal
from app.repositories import account_repo, capability_repo, match_repo
from app.services import scoring_service

def run():
    db = SessionLocal()
    try:
        exporter = capability_repo.get_exporter_capability(db)
        buyers = account_repo.get_all_buyers(db)
        print(f"Running scoring for {len(buyers)} buyers against {exporter.company_name}...")

        for idx, buyer in enumerate(buyers, start=1):
            score = scoring_service.score_match(buyer, exporter, rank=idx)
            print(f"  -> [{score.grade}] #{idx} {buyer.canonical_name}: {score.total_score}/100 (Product:{score.product_fit_score}, Comp:{score.compliance_score}, Lane:{score.lane_economics_score})")

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

            # History: INSERT ONLY
            match_repo.insert_score_history(
                db,
                buyer_id=buyer.id,
                score=score.total_score,
                score_version="v1.0.0",
                drivers=[d.model_dump() for d in score.drivers]
            )

        print("[SUCCESS] All matches re-scored and history logged.")
    finally:
        db.close()

if __name__ == "__main__":
    run()
