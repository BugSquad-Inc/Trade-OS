import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/schemas/capability.py
w("backend/app/schemas/capability.py", """from pydantic import BaseModel
from typing import List, Optional
import uuid

class ExporterCapabilityResponse(BaseModel):
    id: str
    company_name: str
    location: str
    cluster: str
    export_market_focus: List[str]
    material_types: List[str]
    tannage: List[str]
    thickness_range_mm: List[str]
    finish_capabilities: List[str]
    monthly_capacity_sqft: int
    moq_sqft: int
    lead_time_days: int
    sample_lead_time_days: int
    port_of_export: str
    incoterms: List[str]
    certifications: List[str]
    eudr_readiness_score: int
    eudr_gap_summary: Optional[str] = None
""")

# 2. backend/app/schemas/match.py
w("backend/app/schemas/match.py", """from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class DriverItem(BaseModel):
    category: str
    weight: int
    score: float
    title: str
    evidence: str

class ContactSummary(BaseModel):
    full_name: str
    title: Optional[str] = None
    email: Optional[str] = None
    confidence: float
    verification_status: str

class ScoreBreakdown(BaseModel):
    product_fit: float
    compliance: float
    lane_economics: float
    intent_signals: float
    accessibility: float

class MatchCardResponse(BaseModel):
    id: str
    buyer_id: str
    name: str
    legal_name: str
    country_code: str
    country: str
    city: str
    segment: str
    rank: int
    total_score: float
    grade: str
    score_breakdown: ScoreBreakdown
    drivers: List[Dict[str, Any]]
    key_gaps: List[str]
    next_best_action: str
    outreach_angle: str
    status: str
    contact: Optional[ContactSummary] = None
    freight_summary: str
    eudr_readiness_score: int

class MatchListResponse(BaseModel):
    matches: List[MatchCardResponse]
    total_count: int
    generated_at: str
""")

# 3. backend/app/schemas/signal.py
w("backend/app/schemas/signal.py", """from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SignalItem(BaseModel):
    id: str
    entity_id: str
    company_name: str
    category: str
    severity: str
    title: str
    summary: str
    quote: Optional[str] = None
    source_url: Optional[str] = None
    detected_at: str
    score: float
    evidence: Dict[str, Any]

class EUDRChecklistItem(BaseModel):
    item: str
    status: str
    article: str
    gap_detail: Optional[str] = None

class EUDRScorecardResponse(BaseModel):
    entity: str
    readiness_score: int
    status: str
    requirements: List[EUDRChecklistItem]
    top_gap: str
    recommended_action: str

class FreightBenchmarkResponse(BaseModel):
    origin_port: str
    destination_port: str
    mode: str
    container_type: str
    rate_usd: float
    rate_spread: str
    transit_days: str
    port_congestion_index: str
    reroute_risk_notes: Optional[str] = None
    sample_air_transit: str

class SignalListResponse(BaseModel):
    signals: List[SignalItem]
    total_count: int
    eudr_scorecard: EUDRScorecardResponse
    freight_benchmark: FreightBenchmarkResponse
""")

# 4. backend/app/schemas/account.py
w("backend/app/schemas/account.py", """from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ContactDetail(BaseModel):
    id: str
    full_name: str
    title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_primary: bool
    confidence: float
    verification_status: str
    consent_status: str
    legal_basis: str

class ProductDetail(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    hs_code: Optional[str] = None
    material_types: List[str]
    tannage: List[str]
    thickness_range_mm: List[str]
    finish: List[str]

class CertificationDetail(BaseModel):
    id: str
    certification_type: str
    certification_name: str
    issued_by: Optional[str] = None
    status: str
    valid_until: Optional[str] = None

class Account360Response(BaseModel):
    id: str
    canonical_name: str
    legal_name: Optional[str] = None
    domain: Optional[str] = None
    country_code: str
    country: str
    city: Optional[str] = None
    region: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    segment: str
    description: Optional[str] = None
    founded_year: Optional[int] = None
    employee_range: Optional[str] = None
    status: str
    match_score: Optional[float] = None
    grade: Optional[str] = None
    rank: Optional[int] = None
    drivers: List[Dict[str, Any]] = []
    key_gaps: List[str] = []
    next_best_action: Optional[str] = None
    outreach_angle: Optional[str] = None
    contacts: List[ContactDetail] = []
    products: List[ProductDetail] = []
    certifications: List[CertificationDetail] = []
    signals: List[Dict[str, Any]] = []
    eudr_requirements: List[Dict[str, Any]] = []
    lane_economics: Dict[str, Any] = {}
""")

# 5. backend/app/schemas/outreach.py
w("backend/app/schemas/outreach.py", """from pydantic import BaseModel
from typing import Optional

class OutreachRequest(BaseModel):
    buyer_id: str
    tone: str = "Professional"
    contact_name: Optional[str] = None

class OutreachResponse(BaseModel):
    action_id: str
    buyer_id: str
    buyer_name: str
    contact_name: str
    contact_title: str
    tone: str
    subject: str
    body: str
    status: str
""")

# 6. backend/app/api/capability.py
w("backend/app/api/capability.py", """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import capability_repo
from app.schemas.capability import ExporterCapabilityResponse

router = APIRouter(prefix="/api/v1", tags=["Capability"])

@router.get("/capability", response_model=ExporterCapabilityResponse)
def get_capability(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    cap = capability_repo.get_exporter_capability(db)
    if not cap:
        raise HTTPException(status_code=404, detail="Exporter capability not found")

    return ExporterCapabilityResponse(
        id=str(cap.id),
        company_name=cap.company_name,
        location=cap.location,
        cluster=cap.cluster,
        export_market_focus=cap.export_market_focus or ["Germany", "EU"],
        material_types=cap.material_types or [],
        tannage=cap.tannage or [],
        thickness_range_mm=cap.thickness_range_mm or [],
        finish_capabilities=cap.finish_capabilities or [],
        monthly_capacity_sqft=cap.monthly_capacity_sqft,
        moq_sqft=cap.moq_sqft,
        lead_time_days=cap.lead_time_days,
        sample_lead_time_days=cap.sample_lead_time_days,
        port_of_export=cap.port_of_export,
        incoterms=cap.incoterms or [],
        certifications=cap.certifications or [],
        eudr_readiness_score=cap.eudr_readiness_score,
        eudr_gap_summary=cap.eudr_gap_summary
    )
""")

# 7. backend/app/api/matches.py
w("backend/app/api/matches.py", """from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.api.deps import require_api_key
from app.services import match_service
from app.schemas.match import MatchListResponse

router = APIRouter(prefix="/api/v1", tags=["Matches"])

@router.get("/matches", response_model=MatchListResponse)
def get_matches(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    ranked = match_service.list_ranked_matches(db, limit=limit)
    return MatchListResponse(
        matches=ranked,
        total_count=len(ranked),
        generated_at=datetime.utcnow().isoformat() + "Z"
    )
""")

# 8. backend/app/api/signals.py
w("backend/app/api/signals.py", """from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import signal_repo, capability_repo
from app.services import compliance_service, lane_service
from app.schemas.signal import SignalListResponse, SignalItem

router = APIRouter(prefix="/api/v1", tags=["Signals"])

@router.get("/signals", response_model=SignalListResponse)
def get_signals_feed(
    category: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    signals = signal_repo.get_signals(db, category=category, limit=limit)
    exporter = capability_repo.get_exporter_capability(db)
    eudr = compliance_service.calculate_eudr_readiness(exporter)
    lane = lane_service.get_active_lane_benchmark(db)

    signal_items = []
    for s in signals:
        signal_items.append(SignalItem(
            id=str(s.id),
            entity_id=str(s.entity_id),
            company_name=s.company.canonical_name if s.company else "Global",
            category=s.category,
            severity=s.severity,
            title=s.title,
            summary=s.summary,
            quote=s.quote,
            source_url=s.source_url,
            detected_at=s.detected_at.isoformat() if s.detected_at else "",
            score=float(s.score),
            evidence=s.evidence or {}
        ))

    return SignalListResponse(
        signals=signal_items,
        total_count=len(signal_items),
        eudr_scorecard=eudr,
        freight_benchmark=lane
    )
""")

# 9. backend/app/api/accounts.py
w("backend/app/api/accounts.py", """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.api.deps import require_api_key
from app.repositories import account_repo, match_repo, capability_repo
from app.services import compliance_service, lane_service
from app.schemas.account import Account360Response, ContactDetail, ProductDetail, CertificationDetail

router = APIRouter(prefix="/api/v1", tags=["Accounts"])

@router.get("/accounts/{account_id}", response_model=Account360Response)
def get_account_360(
    account_id: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    try:
        company_uuid = uuid.UUID(account_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid account UUID format")

    company = account_repo.get_company_by_id(db, company_uuid)
    if not company:
        raise HTTPException(status_code=404, detail="Account not found")

    match = match_repo.get_match_by_buyer_id(db, company_uuid)
    exporter = capability_repo.get_exporter_capability(db)
    lane = lane_service.get_active_lane_benchmark(db)
    eudr = compliance_service.calculate_eudr_readiness(exporter)

    contacts = [
        ContactDetail(
            id=str(p.id),
            full_name=p.full_name,
            title=p.title,
            email=p.email,
            phone=p.phone,
            linkedin_url=p.linkedin_url,
            is_primary=p.is_primary,
            confidence=float(p.confidence),
            verification_status=p.verification_status,
            consent_status=p.consent_status,
            legal_basis=p.legal_basis
        ) for p in (company.persons or [])
    ]

    products = [
        ProductDetail(
            id=str(pr.id),
            name=pr.name,
            description=pr.description,
            hs_code=pr.hs_code,
            material_types=pr.material_types or [],
            tannage=pr.tannage or [],
            thickness_range_mm=pr.thickness_range_mm or [],
            finish=pr.finish or []
        ) for pr in (company.products or [])
    ]

    certifications = [
        CertificationDetail(
            id=str(c.id),
            certification_type=c.certification_type,
            certification_name=c.certification_name,
            issued_by=c.issued_by,
            status=c.status,
            valid_until=c.valid_to.isoformat() if c.valid_to else None
        ) for c in (company.certifications or [])
    ]

    signals = [
        {
            "id": str(s.id),
            "category": s.category,
            "severity": s.severity,
            "title": s.title,
            "summary": s.summary,
            "detected_at": s.detected_at.isoformat() if s.detected_at else ""
        } for s in (company.signals or [])
    ]

    return Account360Response(
        id=str(company.id),
        canonical_name=company.canonical_name,
        legal_name=company.legal_name or company.canonical_name,
        domain=company.domain,
        country_code=company.country_code,
        country="Germany" if company.country_code == "DE" else company.country_code,
        city=company.city,
        region=company.region,
        website=company.website,
        linkedin_url=company.linkedin_url,
        segment=company.segment,
        description=company.description,
        founded_year=company.founded_year,
        employee_range=company.employee_range,
        status=company.status,
        match_score=float(match.total_score) if match else None,
        grade=match.grade if match else None,
        rank=match.rank if match else None,
        drivers=match.drivers if match else [],
        key_gaps=match.key_gaps if match else [],
        next_best_action=match.next_best_action if match else "Initiate introductory dialogue",
        outreach_angle=match.outreach_angle if match else "Position Butler's Leather as reliable export partner",
        contacts=contacts,
        products=products,
        certifications=certifications,
        signals=signals,
        eudr_requirements=eudr["requirements"],
        lane_economics=lane
    )
""")

# 10. backend/app/api/outreach.py
w("backend/app/api/outreach.py", """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.api.deps import require_api_key
from app.services import outreach_service
from app.schemas.outreach import OutreachRequest, OutreachResponse

router = APIRouter(prefix="/api/v1", tags=["Outreach"])

@router.post("/outreach", response_model=OutreachResponse)
def generate_outreach(
    req: OutreachRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    try:
        buyer_uuid = uuid.UUID(req.buyer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid buyer UUID format")

    try:
        res = outreach_service.generate_personalized_outreach(
            db,
            buyer_id=buyer_uuid,
            tone=req.tone,
            contact_name=req.contact_name
        )
        return OutreachResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
""")

# 11. backend/app/main.py
w("backend/app/main.py", """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import health, capability, matches, signals, accounts, outreach

app = FastAPI(
    title="Trade OS API",
    description="Export Revenue Operating System — Leather & Materials Vertical",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health.router)
app.include_router(capability.router)
app.include_router(matches.router)
app.include_router(signals.router)
app.include_router(accounts.router)
app.include_router(outreach.router)

@app.get("/")
def root():
    return {
        "name": "Trade OS API",
        "status": "running",
        "docs": "/docs",
        "vertical": "Leather & Materials Exporters"
    }
""")

print("[SUCCESS] Part 5 (Schemas, Routers, Main) built successfully")
