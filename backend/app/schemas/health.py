from pydantic import BaseModel
from typing import Optional, Dict, Any

class HealthResponse(BaseModel):
    status: str = "ok"
    environment: str
    database: str
    version: str = "2.0.0"

class LivenessResponse(BaseModel):
    status: str = "live"
    uptime: str = "healthy"
    version: str = "2.0.0"

class ReadinessResponse(BaseModel):
    status: str = "ready"
    environment: str
    database: str
    dependencies: Dict[str, str]
    version: str = "2.0.0"
