from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.config import settings
from app.schemas.health import HealthResponse, LivenessResponse, ReadinessResponse

router = APIRouter(tags=["Health"])

@router.get("/api/v1/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unreachable: {str(e)}"

    return HealthResponse(
        status="ok" if db_status == "connected" else "degraded",
        environment=settings.ENVIRONMENT.value if hasattr(settings.ENVIRONMENT, "value") else str(settings.ENVIRONMENT),
        database=db_status,
        version=settings.APP_VERSION
    )

@router.get("/api/v1/health/live", response_model=LivenessResponse)
def liveness_check():
    """Liveness probe: returns 200 if process is running."""
    return LivenessResponse(
        status="live",
        uptime="healthy",
        version=settings.APP_VERSION
    )

@router.get("/api/v1/health/ready", response_model=ReadinessResponse)
def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe: validates all operational dependencies (PostgreSQL)."""
    db_status = "connected"
    deps = {}
    try:
        db.execute(text("SELECT 1"))
        deps["database"] = "ready"
    except Exception as e:
        db_status = f"unreachable: {str(e)}"
        deps["database"] = "unreachable"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "not_ready", "database": db_status}
        )

    return ReadinessResponse(
        status="ready",
        environment=settings.ENVIRONMENT.value if hasattr(settings.ENVIRONMENT, "value") else str(settings.ENVIRONMENT),
        database=db_status,
        dependencies=deps,
        version=settings.APP_VERSION
    )
