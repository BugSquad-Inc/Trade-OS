from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.lane import TradeCorridorListResponse, TradeCorridorItem

router = APIRouter(prefix='/api/v1/lanes', tags=['Trade Lane Economics'])

TRADE_CORRIDORS = [
    {
        'corridor_id': 'INMAA-DEHAM',
        'origin_port': 'INMAA',
        'origin_city': 'Chennai / Ambur',
        'destination_port': 'DEHAM',
        'destination_city': 'Hamburg',
        'destination_country': 'Germany',
        'transit_days_min': 26,
        'transit_days_max': 34,
        'ocean_freight_usd_feu': 1850.0,
        'landed_cost_eur_sqft': 0.42,
        'port_congestion_index': 'Normal (0.8x benchmark)'
    },
    {
        'corridor_id': 'INMAA-ITGOA',
        'origin_port': 'INMAA',
        'origin_city': 'Chennai / Ranipet',
        'destination_port': 'ITGOA',
        'destination_city': 'Genoa',
        'destination_country': 'Italy',
        'transit_days_min': 22,
        'transit_days_max': 28,
        'ocean_freight_usd_feu': 1720.0,
        'landed_cost_eur_sqft': 0.39,
        'port_congestion_index': 'Low (0.6x benchmark)'
    },
    {
        'corridor_id': 'INCCU-FRLEH',
        'origin_port': 'INCCU',
        'origin_city': 'Kolkata Leather Complex',
        'destination_port': 'FRLEH',
        'destination_city': 'Le Havre',
        'destination_country': 'France',
        'transit_days_min': 28,
        'transit_days_max': 36,
        'ocean_freight_usd_feu': 2100.0,
        'landed_cost_eur_sqft': 0.48,
        'port_congestion_index': 'Moderate (1.1x benchmark)'
    },
    {
        'corridor_id': 'INTUT-ESVLC',
        'origin_port': 'INTUT',
        'origin_city': 'Tuticorin / Vaniyambadi',
        'destination_port': 'ESVLC',
        'destination_city': 'Valencia',
        'destination_country': 'Spain',
        'transit_days_min': 20,
        'transit_days_max': 26,
        'ocean_freight_usd_feu': 1650.0,
        'landed_cost_eur_sqft': 0.37,
        'port_congestion_index': 'Optimal (0.5x benchmark)'
    }
]

@router.get('/corridors', response_model=TradeCorridorListResponse)
def get_trade_corridors(
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    items = [TradeCorridorItem(**c) for c in TRADE_CORRIDORS]
    return TradeCorridorListResponse(total_corridors=len(items), corridors=items)
