from datetime import date, datetime
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
