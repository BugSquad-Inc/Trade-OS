from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CRMExportRequest(BaseModel):
    buyer_id: str
    export_format: str = "hubspot"  # hubspot | salesforce | csv
    include_outreach_sequence: bool = True
    include_eudr_pack: bool = True
    webhook_url: Optional[str] = None

class CRMExportResponse(BaseModel):
    export_id: str
    buyer_id: str
    buyer_name: str
    format: str
    status: str
    payload: Dict[str, Any]
    download_url: Optional[str] = None
    message: str
