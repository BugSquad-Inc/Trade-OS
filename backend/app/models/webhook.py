from datetime import datetime
import uuid
from typing import Optional
from sqlalchemy import Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class WebhookSubscription(Base):
    __tablename__ = 'webhook_subscriptions'
    __table_args__ = {'schema': 'gold'}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_url: Mapped[str] = mapped_column(Text, nullable=False)
    secret_key: Mapped[str] = mapped_column(Text, nullable=False)
    events: Mapped[dict] = mapped_column(JSONB, default=lambda: ['MATCH_QUALIFIED', 'CUSTOMS_SHIPMENT', 'SIGNAL_ALERT'])
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class WebhookEventLog(Base):
    __tablename__ = 'webhook_event_logs'
    __table_args__ = {'schema': 'gold'}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    response_status: Mapped[int] = mapped_column(default=200)
    delivered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
