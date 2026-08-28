import json
from datetime import datetime, timezone

with open("CODEMAP.json", "r", encoding="utf-8") as f:
    data = json.load(f)

data["meta"]["active_sprint"] = "S2"
data["meta"]["completed_sprints"] = ["S1"]
data["modules"]["M9_data_expand"]["status"] = "DONE"

new_entities = {
    "TOS-DB-DATAEXPAND-001": {"name": "SourceSystem", "file": "backend/app/models/ingestion.py", "description": "Bronze source systems and rate limits table"},
    "TOS-DB-DATAEXPAND-002": {"name": "IngestionRun", "file": "backend/app/models/ingestion.py", "description": "Bronze ingestion execution tracking table"},
    "TOS-DB-DATAEXPAND-003": {"name": "RawDocument", "file": "backend/app/models/ingestion.py", "description": "Bronze immutable raw document payload table"},
    "TOS-DB-DATAEXPAND-004": {"name": "RawExtract", "file": "backend/app/models/ingestion.py", "description": "Bronze extracted entity payload table"},
    "TOS-REP-DATAEXPAND-001": {"name": "ingest_repo", "file": "backend/app/repositories/ingest_repo.py", "description": "Repository for bronze source systems and ingestion runs"},
    "TOS-SVC-DATAEXPAND-001": {"name": "entity_resolution_service", "file": "backend/app/services/entity_resolution_service.py", "description": "Entity resolution, legal suffix stripping and company deduplication"},
    "TOS-SVC-DATAEXPAND-002": {"name": "ingestion_service", "file": "backend/app/services/ingestion_service.py", "description": "Multi-source ingestion pipeline for 6 intelligence streams"},
    "TOS-WRK-DATAEXPAND-001": {"name": "nightly_refresh_worker", "file": "backend/app/workers/nightly_refresh_worker.py", "description": "Nightly batch pipeline for ingestion, rescoring and score history logging"},
    "TOS-WRK-DATAEXPAND-002": {"name": "seed_50_buyers", "file": "backend/app/scripts/seed_50_buyers.py", "description": "Multi-source data expansion seeder for 50+ European buyers & 100+ signals"},
    "TOS-SCH-DATAEXPAND-001": {"name": "IngestionStatusResponse / PipelineRefreshResponse", "file": "backend/app/schemas/ingest.py", "description": "Pydantic schemas for ingestion status and pipeline refresh"},
    "TOS-RTE-DATAEXPAND-001": {"name": "get_ingestion_status", "file": "backend/app/api/ingest.py", "description": "GET /api/v1/ingest/status endpoint"},
    "TOS-RTE-DATAEXPAND-002": {"name": "trigger_pipeline_refresh", "file": "backend/app/api/ingest.py", "description": "POST /api/v1/ingest/refresh endpoint"},
    "TOS-FE-DATAEXPAND-001": {"name": "api/ingest.ts", "file": "frontend/src/api/ingest.ts", "description": "Frontend ingestion API client"},
    "TOS-FE-DATAEXPAND-002": {"name": "hooks/useIngest.ts", "file": "frontend/src/hooks/useIngest.ts", "description": "React query hooks for ingestion status and pipeline refresh mutation"},
    "TOS-TST-DATAEXPAND-001": {"name": "test_data_expansion.py", "file": "backend/app/tests/test_data_expansion.py", "description": "Pytest integration tests for multi-source ingestion and resolution"}
}

data["entities"].update(new_entities)
data["meta"]["total_entities"] = len(data["entities"])
data["meta"]["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

with open("CODEMAP.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"[SUCCESS] CODEMAP.json updated with {len(data['entities'])} total registered entities!")
