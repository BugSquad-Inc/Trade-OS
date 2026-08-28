import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories import ingest_repo, signal_repo, account_repo
from app.services import entity_resolution_service

class MultiSourceIngestionService:
    """Orchestrates 6 multi-source ingestion streams into Bronze & Silver."""

    @staticmethod
    def ingest_trade_show_exhibitors(db: Session, expo_name: str, exhibitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        source = ingest_repo.get_or_create_source(
            db,
            name=f"TradeShow_{expo_name}",
            kind="web",
            base_url="https://www.lineapelle-fair.it",
            legal_basis="Public trade fair exhibitor directory"
        )
        run = ingest_repo.create_ingestion_run(db, source.id)

        created_count = 0
        resolved_count = 0
        signals_created = 0

        try:
            for item in exhibitors:
                company, is_new = entity_resolution_service.resolve_or_create_company(db, item["company"])
                if is_new:
                    created_count += 1
                else:
                    resolved_count += 1

                # If exhibitor has intent signal
                if item.get("signal"):
                    sig_data = item["signal"]
                    signal_repo.insert_signal(db, {
                        "entity_id": company.id,
                        "category": sig_data.get("category", "intent"),
                        "severity": sig_data.get("severity", "medium"),
                        "title": sig_data["title"],
                        "summary": sig_data["summary"],
                        "quote": sig_data.get("quote"),
                        "score": sig_data.get("score", 80),
                        "evidence": {
                            "source": expo_name,
                            "booth": item.get("booth"),
                            "collection": item.get("collection_focus")
                        }
                    })
                    signals_created += 1

            stats = {
                "total_records": len(exhibitors),
                "companies_created": created_count,
                "companies_resolved": resolved_count,
                "signals_emitted": signals_created
            }
            ingest_repo.complete_ingestion_run(db, run.id, stats, status="succeeded")
            return stats
        except Exception as e:
            ingest_repo.complete_ingestion_run(db, run.id, stats={}, status="failed", error=str(e))
            raise e

    @staticmethod
    def ingest_regulatory_feed(db: Session, directives: List[Dict[str, Any]]) -> Dict[str, Any]:
        source = ingest_repo.get_or_create_source(
            db,
            name="Regulatory_EUDR_REACH_Monitor",
            kind="rss",
            base_url="https://ec.europa.eu/environment",
            legal_basis="Official Journal of the European Union (Public Access)"
        )
        run = ingest_repo.create_ingestion_run(db, source.id)
        signals_created = 0

        try:
            buyers = account_repo.get_all_buyers(db)
            for d in directives:
                for b in buyers:
                    signal_repo.insert_signal(db, {
                        "entity_id": b.id,
                        "category": "regulatory",
                        "severity": d.get("severity", "high"),
                        "title": f"EUDR Policy Impact: {d['title']}",
                        "summary": d["summary"],
                        "quote": d.get("quote"),
                        "score": 90,
                        "evidence": {"directive": d.get("directive_id", "EU 2023/1115"), "article": d.get("article")}
                    })
                    signals_created += 1

            stats = {"directives_processed": len(directives), "signals_emitted": signals_created}
            ingest_repo.complete_ingestion_run(db, run.id, stats, status="succeeded")
            return stats
        except Exception as e:
            ingest_repo.complete_ingestion_run(db, run.id, stats={}, status="failed", error=str(e))
            raise e
