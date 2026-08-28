from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CustomsShipmentItem(BaseModel):
    id: str
    bol_number: str
    shipment_date: str
    importer_name: str
    exporter_name: str
    origin_port: str
    destination_port: str
    hs_code: str
    product_desc: str
    weight_kg: float
    teu_count: float
    declared_value_usd: Optional[float] = None

class CustomsShipmentsListResponse(BaseModel):
    total_count: int
    shipments: List[CustomsShipmentItem]

class IngestCustomsRequest(BaseModel):
    bol_records: List[Dict[str, Any]]
