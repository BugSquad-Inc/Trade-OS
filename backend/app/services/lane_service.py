from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.lane import TradeLaneBenchmark

def get_active_lane_benchmark(db: Session, origin: str = "INMAA", destination: str = "DEHAM") -> Dict[str, Any]:
    stmt = select(TradeLaneBenchmark).where(
        TradeLaneBenchmark.origin_port == origin,
        TradeLaneBenchmark.destination_port == destination
    ).order_by(TradeLaneBenchmark.effective_start.desc()).limit(1)
    lane = db.execute(stmt).scalar_one_or_none()

    if not lane:
        return {
            "origin_port": "Chennai Port (INMAA)",
            "destination_port": "Hamburg Port (DEHAM)",
            "mode": "sea",
            "container_type": "40HC",
            "rate_usd": 1850.0,
            "rate_spread": "$1,800 - $2,600",
            "transit_days": "26 - 34 ocean days",
            "port_congestion_index": "Normal (1.2 days wait)",
            "reroute_risk_notes": "Suez disruption requires Cape of Good Hope routing (+10-14 days)",
            "sample_air_transit": "2 - 4 days to Frankfurt (FRA)"
        }

    return {
        "origin_port": f"Chennai Port ({lane.origin_port})",
        "destination_port": f"Hamburg Port ({lane.destination_port})",
        "mode": lane.mode,
        "container_type": lane.container_type,
        "rate_usd": float(lane.rate_usd),
        "rate_spread": f"${lane.rate_low_usd:,.0f} - ${lane.rate_high_usd:,.0f}",
        "transit_days": f"{lane.transit_days_min} - {lane.transit_days_max} ocean days",
        "port_congestion_index": lane.port_congestion_index,
        "reroute_risk_notes": lane.reroute_risk_notes or "Suez disruption requires Cape routing (+10-14 days)",
        "sample_air_transit": "2 - 4 days to Frankfurt (FRA)"
    }
