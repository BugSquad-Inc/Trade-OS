import json
from datetime import datetime, timezone

with open("CODEMAP.json", "r", encoding="utf-8") as f:
    data = json.load(f)

data["meta"]["active_sprint"] = "S4"
data["meta"]["completed_sprints"] = ["S1", "S2", "S3", "S4"]

new_entities = {
    "TOS-DB-CUSTOMS-001": {"name": "CustomsShipmentNormalized", "file": "backend/app/models/customs.py", "description": "Silver normalized customs manifest & BOL shipment records table"},
    "TOS-DB-CUSTOMS-002": {"name": "CRMExportLog", "file": "backend/app/models/customs.py", "description": "Gold audit table tracking enterprise CRM exports and webhooks"},
    "TOS-REP-CUSTOMS-001": {"name": "customs_repo", "file": "backend/app/repositories/customs_repo.py", "description": "Repository for normalized customs shipments and BOL filters"},
    "TOS-REP-CRM-001": {"name": "crm_repo", "file": "backend/app/repositories/crm_repo.py", "description": "Repository for logging CRM exports and activity history"},
    "TOS-SVC-CUSTOMS-001": {"name": "CustomsIntelligenceService", "file": "backend/app/services/customs_service.py", "description": "Customs manifest parser, importer entity resolver, and shipment intent signal emitter"},
    "TOS-SVC-CRM-001": {"name": "CRMExportService", "file": "backend/app/services/crm_service.py", "description": "Generates HubSpot, Salesforce, and CSV export payloads from buyer dossiers"},
    "TOS-SCH-CUSTOMS-001": {"name": "CustomsShipmentsListResponse", "file": "backend/app/schemas/customs.py", "description": "Pydantic schemas for customs manifest list and ingest"},
    "TOS-SCH-CRM-001": {"name": "CRMExportResponse", "file": "backend/app/schemas/crm.py", "description": "Pydantic schema for CRM export requests and responses"},
    "TOS-RTE-CUSTOMS-001": {"name": "get_customs_shipments", "file": "backend/app/api/customs.py", "description": "GET /api/v1/customs/shipments endpoint"},
    "TOS-RTE-CRM-001": {"name": "export_buyer_crm", "file": "backend/app/api/crm.py", "description": "POST /api/v1/crm/export endpoint"},
    "TOS-FE-CUSTOMS-001": {"name": "CustomsExplorerView.tsx", "file": "frontend/src/components/customs/CustomsExplorerView.tsx", "description": "Screen 4: Customs Bill of Lading (BOL) Manifest Explorer"},
    "TOS-FE-CRM-001": {"name": "CRMExportModal.tsx", "file": "frontend/src/components/accounts/CRMExportModal.tsx", "description": "1-Click HubSpot / Salesforce / CSV Enterprise Export Modal"},
    "TOS-FE-CUSTOMS-002": {"name": "api/customs.ts", "file": "frontend/src/api/customs.ts", "description": "Frontend customs API client"},
    "TOS-FE-CRM-002": {"name": "api/crm.ts", "file": "frontend/src/api/crm.ts", "description": "Frontend CRM export API client"},
    "TOS-TST-CUSTOMS-001": {"name": "test_customs.py", "file": "backend/app/tests/test_customs.py", "description": "Pytest unit tests for customs manifest retrieval and schema"},
    "TOS-TST-CRM-001": {"name": "test_crm.py", "file": "backend/app/tests/test_crm.py", "description": "Pytest integration tests for HubSpot, Salesforce, and CSV export"},
    "TOS-WRK-CUSTOMS-001": {"name": "seed_customs_data.py", "file": "backend/app/scripts/seed_customs_data.py", "description": "Customs BOL manifest seeder for Indian export corridors"}
}

data["entities"].update(new_entities)
data["meta"]["total_entities"] = len(data["entities"])
data["meta"]["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

with open("CODEMAP.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"[SUCCESS] CODEMAP.json updated with {len(data['entities'])} total registered entities across all 11 modules!")
