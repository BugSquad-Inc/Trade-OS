import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum

class OutreachMode(str, Enum):
    email = "email"
    whatsapp = "whatsapp"
    phone_script = "phone_script"

class OutreachLanguage(str, Enum):
    de = "de" # German (DIN 5008)
    en = "en" # International Business English

class OutreachRequest(BaseModel):
    buyer_id: str
    mode: OutreachMode = OutreachMode.email
    language: OutreachLanguage = OutreachLanguage.en
    tone: str = "Professional" # Professional, Direct, Technical, Relationship
    contact_name: Optional[str] = None

class CompliancePackDoc(BaseModel):
    doc_id: str
    title: str
    document_type: str # lab_test, eudr_due_diligence, environmental_audit, reach_declaration
    issuer: str
    verified_date: str
    file_format: str = "PDF"

class CompliancePackResponse(BaseModel):
    bundle_id: str
    buyer_id: str
    buyer_name: str
    exporter_name: str
    documents: List[CompliancePackDoc]
    total_documents: int
    generated_at: str
    download_url: str

class OutreachResponse(BaseModel):
    action_id: str
    buyer_id: str
    buyer_name: str
    contact_name: str
    contact_title: str
    mode: OutreachMode
    language: OutreachLanguage
    tone: str
    subject: str
    body: str
    why_matches_you: List[str]
    compliance_pack_docs: List[str]
    status: str

    model_config = ConfigDict(from_attributes=True)
