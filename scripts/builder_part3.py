import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. backend/app/models/base.py
w("backend/app/models/base.py", """from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import MetaData

class Base(DeclarativeBase):
    pass
""")

# 2. backend/app/models/company.py
w("backend/app/models/company.py", """from datetime import datetime
import uuid
from typing import List, Optional
from sqlalchemy import String, Integer, Numeric, Boolean, Text, DateTime, ForeignKey, CHAR, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class EntityCompany(Base):
    __tablename__ = "entity_company"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    canonical_name: Mapped[str] = mapped_column(Text, nullable=False)
    legal_name: Mapped[Optional[str]] = mapped_column(Text)
    domain: Mapped[Optional[str]] = mapped_column(Text)
    country_code: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    city: Mapped[Optional[str]] = mapped_column(Text)
    region: Mapped[Optional[str]] = mapped_column(Text)
    postal_code: Mapped[Optional[str]] = mapped_column(Text)
    website: Mapped[Optional[str]] = mapped_column(Text)
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text)
    segment: Mapped[str] = mapped_column(Text, default="Leather goods")
    description: Mapped[Optional[str]] = mapped_column(Text)
    founded_year: Mapped[Optional[int]] = mapped_column(Integer)
    employee_range: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="active")
    confidence: Mapped[float] = mapped_column(Numeric, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    persons: Mapped[List["EntityPerson"]] = relationship("EntityPerson", back_populates="company", cascade="all, delete-orphan")
    products: Mapped[List["EntityProduct"]] = relationship("EntityProduct", back_populates="company", cascade="all, delete-orphan")
    certifications: Mapped[List["EntityCertification"]] = relationship("EntityCertification", back_populates="company", cascade="all, delete-orphan")
    signals: Mapped[List["Signal"]] = relationship("Signal", back_populates="company", cascade="all, delete-orphan")
    match_candidate: Mapped[Optional["MatchCandidate"]] = relationship("MatchCandidate", back_populates="company", uselist=False)

class EntityPerson(Base):
    __tablename__ = "entity_person"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(Text)
    email: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(Text)
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence: Mapped[float] = mapped_column(Numeric, default=0.8)
    verification_status: Mapped[str] = mapped_column(Text, default="illustrative")
    consent_status: Mapped[str] = mapped_column(Text, default="legitimate_interest")
    legal_basis: Mapped[str] = mapped_column(Text, default="B2B legitimate interest under GDPR Art. 6(1)(f)")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="persons")

class EntityProduct(Base):
    __tablename__ = "entity_product"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    hs_code: Mapped[Optional[str]] = mapped_column(Text)
    material_types: Mapped[dict] = mapped_column(JSONB, default=list)
    tannage: Mapped[dict] = mapped_column(JSONB, default=list)
    thickness_range_mm: Mapped[dict] = mapped_column(JSONB, default=list)
    finish: Mapped[dict] = mapped_column(JSONB, default=list)
    spec: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="products")
""")

# 3. backend/app/models/compliance.py
w("backend/app/models/compliance.py", """from datetime import date, datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class EntityCertification(Base):
    __tablename__ = "entity_certification"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    certification_type: Mapped[str] = mapped_column(Text, nullable=False)
    certification_name: Mapped[str] = mapped_column(Text, nullable=False)
    issued_by: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="active")
    valid_from: Mapped[Optional[date]] = mapped_column(Date)
    valid_to: Mapped[Optional[date]] = mapped_column(Date)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="certifications")
""")

# 4. backend/app/models/lane.py
w("backend/app/models/lane.py", """from datetime import date, datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Integer, Numeric, Date, DateTime, CHAR, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class TradeLaneBenchmark(Base):
    __tablename__ = "trade_lane_benchmark"
    __table_args__ = {"schema": "silver"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin_country: Mapped[str] = mapped_column(CHAR(2), default="IN")
    origin_port: Mapped[str] = mapped_column(Text, default="INMAA")
    destination_country: Mapped[str] = mapped_column(CHAR(2), default="DE")
    destination_port: Mapped[str] = mapped_column(Text, default="DEHAM")
    mode: Mapped[str] = mapped_column(Text, default="sea")
    container_type: Mapped[str] = mapped_column(Text, default="40HC")
    rate_usd: Mapped[float] = mapped_column(Numeric, nullable=False)
    rate_low_usd: Mapped[float] = mapped_column(Numeric, nullable=False)
    rate_high_usd: Mapped[float] = mapped_column(Numeric, nullable=False)
    transit_days_min: Mapped[int] = mapped_column(Integer, nullable=False)
    transit_days_max: Mapped[int] = mapped_column(Integer, nullable=False)
    port_congestion_index: Mapped[str] = mapped_column(Text, default="Normal (1.2 days wait)")
    reroute_risk_notes: Mapped[Optional[str]] = mapped_column(Text)
    effective_start: Mapped[date] = mapped_column(Date, default=date.today)
    effective_end: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
""")

# 5. backend/app/models/exporter.py
w("backend/app/models/exporter.py", """from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class ExporterCapability(Base):
    __tablename__ = "exporter_capability"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(Text, nullable=False)
    cluster: Mapped[str] = mapped_column(Text, nullable=False)
    export_market_focus: Mapped[dict] = mapped_column(JSONB, default=lambda: ["Germany", "EU"])
    material_types: Mapped[dict] = mapped_column(JSONB, default=lambda: ["finished bovine leather", "goat nappa", "crust"])
    tannage: Mapped[dict] = mapped_column(JSONB, default=lambda: ["vegetable", "chrome", "chrome-free"])
    thickness_range_mm: Mapped[dict] = mapped_column(JSONB, default=lambda: ["0.8-1.0", "1.2-1.4", "1.6-2.2"])
    finish_capabilities: Mapped[dict] = mapped_column(JSONB, default=lambda: ["aniline", "semi-aniline", "pigmented", "pull-up"])
    monthly_capacity_sqft: Mapped[int] = mapped_column(Integer, default=50000)
    moq_sqft: Mapped[int] = mapped_column(Integer, default=3000)
    lead_time_days: Mapped[int] = mapped_column(Integer, default=35)
    sample_lead_time_days: Mapped[int] = mapped_column(Integer, default=10)
    port_of_export: Mapped[str] = mapped_column(Text, default="Chennai Port (INMAA)")
    incoterms: Mapped[dict] = mapped_column(JSONB, default=lambda: ["FOB", "CIF", "EXW"])
    certifications: Mapped[dict] = mapped_column(JSONB, default=lambda: ["LWG Gold", "ISO 9001", "ISO 14001", "REACH"])
    eudr_readiness_score: Mapped[int] = mapped_column(Integer, default=68)
    eudr_gap_summary: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
""")

# 6. backend/app/models/signal.py
w("backend/app/models/signal.py", """from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import Text, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Signal(Base):
    __tablename__ = "signal"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(Text, default="medium")
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    quote: Mapped[Optional[str]] = mapped_column(Text)
    source_url: Mapped[Optional[str]] = mapped_column(Text)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    score: Mapped[float] = mapped_column(Numeric, default=0)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="signals")
    evidence_items: Mapped[List["SignalEvidence"]] = relationship("SignalEvidence", back_populates="signal", cascade="all, delete-orphan")

class SignalEvidence(Base):
    __tablename__ = "signal_evidence"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.signal.id", ondelete="CASCADE"), nullable=False)
    document_url: Mapped[Optional[str]] = mapped_column(Text)
    quote: Mapped[Optional[str]] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Numeric, default=0.9)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    signal: Mapped["Signal"] = relationship("Signal", back_populates="evidence_items")
""")

# 7. backend/app/models/match.py
w("backend/app/models/match.py", """from datetime import datetime
import uuid
from typing import Optional, List
from sqlalchemy import Text, Integer, Numeric, Boolean, DateTime, ForeignKey, CHAR, BigInteger, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class MatchProfile(Base):
    __tablename__ = "match_profile"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    exporter_capability_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.exporter_capability.id"))
    objective: Mapped[str] = mapped_column(Text, default="find_buyers")
    criteria: Mapped[dict] = mapped_column(JSONB, default=dict)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    candidates: Mapped[List["MatchCandidate"]] = relationship("MatchCandidate", back_populates="profile", cascade="all, delete-orphan")

class MatchCandidate(Base):
    __tablename__ = "match_candidate"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.match_profile.id", ondelete="CASCADE"))
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    product_fit_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    compliance_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    lane_economics_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    intent_signals_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    accessibility_score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    grade: Mapped[str] = mapped_column(CHAR(1), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    score_version: Mapped[str] = mapped_column(Text, default="v1.0.0")
    drivers: Mapped[dict] = mapped_column(JSONB, default=list)
    key_gaps: Mapped[dict] = mapped_column(JSONB, default=list)
    next_best_action: Mapped[str] = mapped_column(Text, nullable=False)
    outreach_angle: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, default="suggested")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    profile: Mapped[Optional["MatchProfile"]] = relationship("MatchProfile", back_populates="candidates")
    company: Mapped["EntityCompany"] = relationship("EntityCompany", back_populates="match_candidate")

class MatchScoreHistory(Base):
    __tablename__ = "match_score_history"
    __table_args__ = {"schema": "gold"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id"), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)
    score_version: Mapped[str] = mapped_column(Text, nullable=False)
    drivers: Mapped[dict] = mapped_column(JSONB, nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class Action(Base):
    __tablename__ = "actions"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    buyer_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("silver.entity_company.id", ondelete="CASCADE"), nullable=False)
    action_type: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, default="generated")
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class AuditEvent(Base):
    __tablename__ = "audit_event"
    __table_args__ = {"schema": "audit"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    object_type: Mapped[str] = mapped_column(Text, nullable=False)
    object_id: Mapped[Optional[str]] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
""")

# 8. backend/app/models/__init__.py
w("backend/app/models/__init__.py", """from app.models.base import Base
from app.models.company import EntityCompany, EntityPerson, EntityProduct
from app.models.compliance import EntityCertification
from app.models.lane import TradeLaneBenchmark
from app.models.exporter import ExporterCapability
from app.models.signal import Signal, SignalEvidence
from app.models.match import MatchProfile, MatchCandidate, MatchScoreHistory, Action, AuditEvent

__all__ = [
    "Base",
    "EntityCompany",
    "EntityPerson",
    "EntityProduct",
    "EntityCertification",
    "TradeLaneBenchmark",
    "ExporterCapability",
    "Signal",
    "SignalEvidence",
    "MatchProfile",
    "MatchCandidate",
    "MatchScoreHistory",
    "Action",
    "AuditEvent"
]
""")

print("[SUCCESS] Part 3 (ORM Models) built successfully")
