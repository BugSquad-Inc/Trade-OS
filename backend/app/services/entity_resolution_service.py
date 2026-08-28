import re
import unicodedata
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.company import EntityCompany

def normalize_company_name(name: str) -> str:
    """Normalizes legal forms, spaces, accents for fuzzy matching."""
    normalized = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    normalized = normalized.lower()
    # Replace punctuation and special characters with spaces
    normalized = re.sub(r'[&,./\-_]', ' ', normalized)
    # Remove common German/European legal suffixes
    tokens = [
        r'\bgmbh\s+co\s+kg\b', r'\bgmbh\b', r'\bag\b', r'\bco\s+kg\b',
        r'\be\s+k\b', r'\bs\s+a\b', r'\bs\s+p\s+a\b', r'\bs\s+r\s+l\b', r'\bs\s+l\b',
        r'\binc\b', r'\bltd\b', r'\bcorp\b', r'\bplc\b', r'\bsas\b'
    ]
    for s in tokens:
        normalized = re.sub(s, ' ', normalized)
    normalized = re.sub(r'[^a-z0-9\s]', ' ', normalized)
    return re.sub(r'\s+', ' ', normalized).strip()

def resolve_or_create_company(db: Session, company_data: Dict[str, Any]) -> tuple[EntityCompany, bool]:
    """Resolves company by domain, exact canonical_name, or normalized key."""
    raw_name = company_data.get("canonical_name", "").strip()
    domain = company_data.get("domain", "").strip().lower() if company_data.get("domain") else None
    country_code = company_data.get("country_code", "DE").upper()

    company = None
    if domain:
        stmt = select(EntityCompany).where(EntityCompany.domain == domain)
        company = db.execute(stmt).scalar_one_or_none()

    if not company and raw_name:
        stmt = select(EntityCompany).where(
            EntityCompany.canonical_name == raw_name,
            EntityCompany.country_code == country_code
        )
        company = db.execute(stmt).scalar_one_or_none()

    is_new = False
    if not company:
        is_new = True
        company = EntityCompany(
            canonical_name=raw_name,
            legal_name=company_data.get("legal_name", raw_name),
            domain=domain,
            country_code=country_code,
            city=company_data.get("city"),
            region=company_data.get("region"),
            postal_code=company_data.get("postal_code"),
            website=company_data.get("website"),
            linkedin_url=company_data.get("linkedin_url"),
            segment=company_data.get("segment", "Leather goods"),
            description=company_data.get("description"),
            founded_year=company_data.get("founded_year"),
            employee_range=company_data.get("employee_range"),
            status=company_data.get("status", "active"),
            confidence=company_data.get("confidence", 0.9)
        )
        db.add(company)
        db.commit()
        db.refresh(company)
    else:
        # Update fields if new data has higher fidelity
        for key in ["legal_name", "city", "region", "website", "linkedin_url", "segment", "description"]:
            if company_data.get(key) and not getattr(company, key, None):
                setattr(company, key, company_data[key])
        db.commit()
        db.refresh(company)

    return company, is_new
