from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TradeCorridorItem(BaseModel):
    corridor_id: str
    origin_port: str
    origin_city: str
    destination_port: str
    destination_city: str
    destination_country: str
    transit_days_min: int
    transit_days_max: int
    ocean_freight_usd_feu: float
    landed_cost_eur_sqft: float
    port_congestion_index: str

class TradeCorridorListResponse(BaseModel):
    total_corridors: int
    corridors: List[TradeCorridorItem]
