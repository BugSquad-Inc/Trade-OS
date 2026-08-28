from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Dict, Any
import uuid
from app.models.customs import CRMExportLog

def log_crm_export(db: Session, buyer_id: uuid.UUID, export_format: str, exported_data: Dict[str, Any], destination_target: str = None) -> CRMExportLog:
    log_entry = CRMExportLog(
        id=uuid.uuid4(),
        buyer_id=buyer_id,
        export_format=export_format,
        status="success",
        exported_data=exported_data,
        destination_target=destination_target
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def list_recent_crm_exports(db: Session, limit: int = 20) -> List[CRMExportLog]:
    stmt = select(CRMExportLog).order_by(desc(CRMExportLog.created_at)).limit(limit)
    return list(db.execute(stmt).scalars().all())
