import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.document import TradeDocument, DocumentType

def list_documents(db: Session, doc_type: Optional[str] = None, opportunity_id: Optional[uuid.UUID] = None) -> List[TradeDocument]:
    """List trade documents with optional type or opportunity filters."""
    stmt = select(TradeDocument).order_by(TradeDocument.created_at.desc())
    if doc_type:
        stmt = stmt.where(TradeDocument.doc_type == doc_type)
    if opportunity_id:
        stmt = stmt.where(TradeDocument.opportunity_id == opportunity_id)
    return list(db.execute(stmt).scalars().all())

def get_document_by_id(db: Session, doc_id: uuid.UUID) -> Optional[TradeDocument]:
    """Get single document metadata by ID."""
    stmt = select(TradeDocument).where(TradeDocument.id == doc_id)
    return db.execute(stmt).scalar_one_or_none()

def create_document(db: Session, data: Dict[str, Any]) -> TradeDocument:
    """Register metadata and vault reference for an export document."""
    doc = TradeDocument(
        tenant_id=data.get("tenant_id"),
        opportunity_id=data.get("opportunity_id"),
        shipment_id=data.get("shipment_id"),
        product_version_id=data.get("product_version_id"),
        doc_type=data["doc_type"],
        title=data["title"],
        file_name=data["file_name"],
        file_size_bytes=data.get("file_size_bytes", 102400),
        file_hash_sha256=data.get("file_hash_sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        mime_type=data.get("mime_type", "application/pdf"),
        storage_uri=data.get("storage_uri", "s3://tradeos-vault/docs/sample.pdf"),
        status=data.get("status", "verified"),
        metadata_json=data.get("metadata", {})
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc
