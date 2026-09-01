import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base

class UserRole(str, Enum):
    owner = "owner"
    sales = "sales"
    compliance = "compliance"
    finance = "finance"
    logistics = "logistics"
    analyst = "analyst"
    admin = "admin"
    auditor = "auditor" # Backward-compatible alias for analyst/compliance

class Tenant(Base):
    __tablename__ = "tenant"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    country_code: Mapped[str] = mapped_column(String(2), default="IN", nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="professional") # starter, professional, enterprise
    status: Mapped[str] = mapped_column(String(50), default="active") # active, suspended, trial
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    memberships = relationship("TenantMembership", back_populates="tenant", cascade="all, delete-orphan")
    users = relationship("UserAccount", back_populates="tenant", cascade="all, delete-orphan")

class UserAccount(Base):
    __tablename__ = "user_account"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.tenant.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role_enum", schema="gold", values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.sales,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    oidc_sub: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # OAuth/OIDC subject ID
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    tenant = relationship("Tenant", back_populates="users")
    memberships = relationship("TenantMembership", back_populates="user", cascade="all, delete-orphan")

class TenantMembership(Base):
    __tablename__ = "tenant_membership"
    __table_args__ = {"schema": "gold"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.tenant.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("gold.user_account.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role_enum", schema="gold", values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.sales,
        nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="active") # active, invited, revoked
    invited_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    tenant = relationship("Tenant", back_populates="memberships")
    user = relationship("UserAccount", back_populates="memberships")
