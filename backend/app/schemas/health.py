from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str = "ok"
    environment: str
    database: str
    version: str = "1.0.0"
