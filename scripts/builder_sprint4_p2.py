import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/schemas/customs.py
w("backend/app/schemas/customs.py", """from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CustomsShipmentItem(BaseModel):
    id: str
    bol_number: str
    shipment_date: str
    importer_name: str
    exporter_name: str
    origin_port: str
    destination_port: str
    hs_code: str
    product_desc: str
    weight_kg: float
    teu_count: float
    declared_value_usd: Optional[float] = None

class CustomsShipmentsListResponse(BaseModel):
    total_count: int
    shipments: List[CustomsShipmentItem]

class IngestCustomsRequest(BaseModel):
    bol_records: List[Dict[str, Any]]
""")

# 2. backend/app/schemas/crm.py
w("backend/app/schemas/crm.py", """from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CRMExportRequest(BaseModel):
    buyer_id: str
    export_format: str = "hubspot"  # hubspot | salesforce | csv
    include_outreach_sequence: bool = True
    include_eudr_pack: bool = True
    webhook_url: Optional[str] = None

class CRMExportResponse(BaseModel):
    export_id: str
    buyer_id: str
    buyer_name: str
    format: str
    status: str
    payload: Dict[str, Any]
    download_url: Optional[str] = None
    message: str
""")

# 3. backend/app/services/customs_service.py
w("backend/app/services/customs_service.py", """from datetime import datetime, date
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories import customs_repo, account_repo, signal_repo
from app.services import entity_resolution_service

class CustomsIntelligenceService:
    \"\"\"Parses customs manifests, matches importers, and generates volume & intent signals.\"\"\"

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
""")

# 4. backend/app/services/crm_service.py
w("backend/app/services/crm_service.py", """import uuid
import io
import csv
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.repositories import account_repo, match_repo, capability_repo, crm_repo
from app.services import outreach_service

class CRMExportService:
    \"\"\"Generates enterprise exports for HubSpot, Salesforce, and CSV.\"\"\"

    @staticmethod
    def export_buyer_dossier(
        db: Session,
        buyer_id: uuid.UUID,
        export_format: str = "hubspot"
    ) -> Dict[str, Any]:
        company = account_repo.get_company_by_id(db, buyer_id)
        if not company:
            raise ValueError("Buyer not found")

        exporter = capability_repo.get_exporter_capability(db)
        match = match_repo.get_match_by_buyer_id(db, buyer_id)
        outreach = outreach_service.generate_outreach(company, exporter, tone="Professional")

        primary_contact = next((c for c in company.persons if c.is_primary), company.persons[0] if company.persons else None)

        if export_format.lower() == "hubspot":
            payload = {
                "company_properties": {
                    "name": company.canonical_name,
                    "domain": company.domain,
                    "city": company.city,
                    "country": company.country_code,
                    "tradeos_match_score": float(match.total_score) if match else 85.0,
                    "tradeos_match_grade": match.grade if match else "A",
                    "tradeos_target_segment": company.segment,
                    "tradeos_eudr_readiness": "68/100 (Article 4 DDS Required)"
                },
                "contact_properties": {
                    "firstname": primary_contact.full_name.split()[0] if primary_contact else "Procurement",
                    "lastname": " ".join(primary_contact.full_name.split()[1:]) if primary_contact and len(primary_contact.full_name.split()) > 1 else "Lead",
                    "email": primary_contact.email if primary_contact else "",
                    "jobtitle": primary_contact.title if primary_contact else "Leather Sourcing Manager",
                    "gdpr_legal_basis": "B2B Legitimate Interest Art. 6(1)(f)"
                },
                "deal_proposal": {
                    "dealname": f"Butler's Leather → {company.canonical_name} (Trial Container)",
                    "pipeline": "Export Sales Pipeline",
                    "stage": "Qualified Match",
                    "amount": "45000",
                    "currency": "USD",
                    "initial_outreach_subject": outreach.subject,
                    "initial_outreach_body": outreach.body
                }
            }
        elif export_format.lower() == "salesforce":
            payload = {
                "Lead": {
                    "Company": company.canonical_name,
                    "FirstName": primary_contact.full_name.split()[0] if primary_contact else "Procurement",
                    "LastName": " ".join(primary_contact.full_name.split()[1:]) if primary_contact and len(primary_contact.full_name.split()) > 1 else "Lead",
                    "Email": primary_contact.email if primary_contact else "",
                    "Title": primary_contact.title if primary_contact else "Leather Sourcing Lead",
                    "Country": company.country_code,
                    "City": company.city,
                    "Status": "Working - Contacted",
                    "TradeOS_Score__c": float(match.total_score) if match else 85.0,
                    "Description": f"Export match: {company.segment}. Outreach Draft:\\n{outreach.body}"
                }
            }
        else:  # CSV format
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Company Name", "Country", "City", "Match Score", "Grade", "Contact Name", "Contact Email", "Outreach Subject"])
            writer.writerow([
                company.canonical_name,
                company.country_code,
                company.city,
                float(match.total_score) if match else 85.0,
                match.grade if match else "A",
                primary_contact.full_name if primary_contact else "",
                primary_contact.email if primary_contact else "",
                outreach.subject
            ])
            payload = {"csv_content": output.getvalue()}

        # Log export
        log_entry = crm_repo.log_crm_export(db, buyer_id, export_format, payload)

        return {
            "export_id": str(log_entry.id),
            "buyer_id": str(buyer_id),
            "buyer_name": company.canonical_name,
            "format": export_format,
            "status": "success",
            "payload": payload,
            "message": f"Successfully generated {export_format.upper()} export payload for {company.canonical_name}."
        }
""")

# 5. backend/app/api/customs.py
w("backend/app/api/customs.py", """from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import customs_repo
from app.schemas.customs import CustomsShipmentsListResponse, CustomsShipmentItem, IngestCustomsRequest
from app.services.customs_service import CustomsIntelligenceService

router = APIRouter(prefix="/api/v1/customs", tags=["Customs & BOL Flows"])

@router.get("/shipments", response_model=CustomsShipmentsListResponse)
def get_customs_shipments(
    importer_id: Optional[str] = None,
    hs_code: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    imp_uuid = uuid.UUID(importer_id) if importer_id else None
    shipments = customs_repo.list_customs_shipments(db, importer_id=imp_uuid, hs_code=hs_code, limit=limit)
    items = [
        CustomsShipmentItem(
            id=str(s.id),
            bol_number=s.bol_number,
            shipment_date=s.shipment_date.isoformat(),
            importer_name=s.importer_raw_name,
            exporter_name=s.exporter_raw_name,
            origin_port=s.origin_port,
            destination_port=s.destination_port,
            hs_code=s.hs_code,
            product_desc=s.product_desc,
            weight_kg=float(s.weight_kg),
            teu_count=float(s.teu_count),
            declared_value_usd=float(s.declared_value_usd) if s.declared_value_usd else None
        ) for s in shipments
    ]
    return CustomsShipmentsListResponse(total_count=len(items), shipments=items)

@router.post("/ingest")
def ingest_customs_records(
    req: IngestCustomsRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    res = CustomsIntelligenceService.ingest_bol_records(db, req.bol_records)
    return {"status": "succeeded", "stats": res}
""")

# 6. backend/app/api/crm.py
w("backend/app/api/crm.py", """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.crm import CRMExportRequest, CRMExportResponse
from app.services.crm_service import CRMExportService

router = APIRouter(prefix="/api/v1/crm", tags=["CRM & Enterprise Export"])

@router.post("/export", response_model=CRMExportResponse)
def export_buyer_crm(
    req: CRMExportRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    try:
        b_uuid = uuid.UUID(req.buyer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid buyer UUID")

    try:
        res = CRMExportService.export_buyer_dossier(db, b_uuid, export_format=req.export_format)
        return CRMExportResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
""")

print("[SUCCESS] Phase 4 Part 2 (Customs & CRM Services and API Routes) built successfully")
