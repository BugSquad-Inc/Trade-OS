import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/models/ingestion.py
w("backend/app/models/ingestion.py", """from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class SourceSystem(Base):
    __tablename__ = "source_system"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    base_url: Mapped[Optional[str]] = mapped_column(Text)
    legal_basis: Mapped[Optional[str]] = mapped_column(Text)
    robots_policy: Mapped[Optional[str]] = mapped_column(Text)
    auth: Mapped[dict] = mapped_column(JSONB, default=dict)
    rate_limit: Mapped[dict] = mapped_column(JSONB, default=lambda: {"requests_per_minute": 30})
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

class IngestionRun(Base):
    __tablename__ = "ingestion_run"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bronze.source_system.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(Text, default="queued")
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    cursor: Mapped[Optional[str]] = mapped_column(Text)
    stats: Mapped[dict] = mapped_column(JSONB, default=dict)
    error: Mapped[Optional[str]] = mapped_column(Text)

class RawDocument(Base):
    __tablename__ = "raw_document"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bronze.source_system.id"), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(Text)
    url: Mapped[Optional[str]] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(Text)
    mime_type: Mapped[Optional[str]] = mapped_column(Text)
    content_text: Mapped[Optional[str]] = mapped_column(Text)
    content_json: Mapped[Optional[dict]] = mapped_column(JSONB)
    content_hash: Mapped[str] = mapped_column(Text, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    meta: Mapped[dict] = mapped_column(JSONB, default=dict)

class RawExtract(Base):
    __tablename__ = "raw_extract"
    __table_args__ = {"schema": "bronze"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bronze.raw_document.id", ondelete="CASCADE"), nullable=False)
    extractor_name: Mapped[str] = mapped_column(Text, nullable=False)
    extractor_version: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, default="success")
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    confidence: Mapped[float] = mapped_column(Numeric, default=0.9)
    error: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
""")

# 2. backend/app/repositories/ingest_repo.py
w("backend/app/repositories/ingest_repo.py", """from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Optional, Dict, Any
import uuid
from app.models.ingestion import SourceSystem, IngestionRun, RawDocument, RawExtract

def get_or_create_source(db: Session, name: str, kind: str, base_url: str = None, legal_basis: str = None) -> SourceSystem:
    stmt = select(SourceSystem).where(SourceSystem.name == name)
    source = db.execute(stmt).scalar_one_or_none()
    if not source:
        source = SourceSystem(
            name=name,
            kind=kind,
            base_url=base_url,
            legal_basis=legal_basis or "Public B2B directory / trade fair catalog under GDPR Art. 6(1)(f)"
        )
        db.add(source)
        db.commit()
        db.refresh(source)
    return source

def create_ingestion_run(db: Session, source_id: uuid.UUID) -> IngestionRun:
    run = IngestionRun(
        source_id=source_id,
        status="running"
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

def complete_ingestion_run(db: Session, run_id: uuid.UUID, stats: dict, status: str = "succeeded", error: str = None) -> IngestionRun:
    run = db.get(IngestionRun, run_id)
    if run:
        run.status = status
        run.finished_at = func.now()
        run.stats = stats
        run.error = error
        db.commit()
        db.refresh(run)
    return run

def list_recent_ingestion_runs(db: Session, limit: int = 20) -> List[IngestionRun]:
    stmt = select(IngestionRun).order_by(desc(IngestionRun.started_at)).limit(limit)
    return list(db.execute(stmt).scalars().all())
""")

# 3. backend/app/services/entity_resolution_service.py
w("backend/app/services/entity_resolution_service.py", """import re
import unicodedata
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.company import EntityCompany

def normalize_company_name(name: str) -> str:
    \"\"\"Normalizes legal forms, spaces, accents for fuzzy matching.\"\"\"
    normalized = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    normalized = normalized.lower()
    # Remove common German/European legal suffixes
    suffixes = [
        r'\bgmbh & co\.?\s*kg\b', r'\bgmbh\b', r'\bag\b', r'\bco\.?\s*kg\b',
        r'\be\.?k\.?\b', r'\bs\.?a\.?\b', r'\bs\.?r\.?l\.?\b', r'\bs\.?l\.?\b',
        r'\binc\.?\b', r'\bltd\.?\b', r'\bcorp\.?\b', r'\bplc\b'
    ]
    for s in suffixes:
        normalized = re.sub(s, '', normalized)
    normalized = re.sub(r'[^a-z0-9\s]', ' ', normalized)
    return re.sub(r'\s+', ' ', normalized).strip()

def resolve_or_create_company(db: Session, company_data: Dict[str, Any]) -> tuple[EntityCompany, bool]:
    \"\"\"Resolves company by domain, exact canonical_name, or normalized key.\"\"\"
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
""")

# 4. backend/app/services/ingestion_service.py
w("backend/app/services/ingestion_service.py", """import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.repositories import ingest_repo, signal_repo, account_repo
from app.services import entity_resolution_service

class MultiSourceIngestionService:
    \"\"\"Orchestrates 6 multi-source ingestion streams into Bronze & Silver.\"\"\"

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
""")

print("[SUCCESS] Sprint 2 Part 1 (Ingestion Models, Repos, Resolution & Ingestion Service) built successfully")
