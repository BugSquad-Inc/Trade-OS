from datetime import datetime, date
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories import customs_repo, account_repo, signal_repo
from app.services import entity_resolution_service

class CustomsIntelligenceService:
    """Parses customs manifests, matches importers, and generates volume & intent signals."""

    @staticmethod
    def ingest_bol_records(db: Session, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        ingested = 0
        signals_emitted = 0

        for r in records:
            # Resolve importer company
            importer_name = r.get("importer_raw_name", "")
            matched_company = None
            if importer_name:
                company_payload = {
                    "canonical_name": importer_name,
                    "country_code": r.get("destination_country", "DE")
                }
                matched_company, _ = entity_resolution_service.resolve_or_create_company(db, company_payload)

            shipment_date_val = r.get("shipment_date")
            if isinstance(shipment_date_val, str):
                shipment_date_val = date.fromisoformat(shipment_date_val)

            shipment = customs_repo.insert_customs_shipment(db, {
                "bol_number": r["bol_number"],
                "shipment_date": shipment_date_val,
                "importer_id": matched_company.id if matched_company else None,
                "importer_raw_name": importer_name,
                "exporter_raw_name": r.get("exporter_raw_name", "Indian Leather Exporter"),
                "origin_country": r.get("origin_country", "IN"),
                "origin_port": r.get("origin_port", "INMAA"),
                "destination_country": r.get("destination_country", "DE"),
                "destination_port": r.get("destination_port", "DEHAM"),
                "hs_code": r.get("hs_code", "4107"),
                "product_desc": r.get("product_desc", "Finished bovine leather"),
                "weight_kg": r.get("weight_kg", 5400.0),
                "teu_count": r.get("teu_count", 1.0),
                "declared_value_usd": r.get("declared_value_usd", 45000.0),
                "raw_payload": r
            })
            ingested += 1

            # Emit Customs Shipment Signal
            if matched_company:
                signal_repo.insert_signal(db, {
                    "entity_id": matched_company.id,
                    "category": "intent",
                    "severity": "high",
                    "title": f"Customs BOL: {importer_name} imported {shipment.teu_count} FEU of HS {shipment.hs_code}",
                    "summary": f"Manifest record confirmed {shipment.weight_kg}kg shipment from {shipment.origin_port} to {shipment.destination_port}.",
                    "quote": f"Bill of Lading {shipment.bol_number} — {shipment.product_desc}",
                    "score": 92,
                    "evidence": {
                        "bol_number": shipment.bol_number,
                        "origin_port": shipment.origin_port,
                        "destination_port": shipment.destination_port,
                        "weight_kg": float(shipment.weight_kg),
                        "teu_count": float(shipment.teu_count)
                    }
                })
                signals_emitted += 1

        return {"ingested_count": ingested, "signals_emitted": signals_emitted}
