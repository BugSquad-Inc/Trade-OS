from fastapi import APIRouter, Depends, HTTPException
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
