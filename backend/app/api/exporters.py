from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.exporter import ExporterProfileResponse, ExporterProfileUpdate, ExporterOnboardingStepRequest, ReadinessGapResponse
from app.repositories import exporter_repo

router = APIRouter(prefix="/api/v1/exporters", tags=["Exporters & Onboarding"], dependencies=[Depends(require_api_key)])

@router.get("/profile", response_model=ExporterProfileResponse)
def get_profile(db: Session = Depends(get_db)):
    """Retrieve full exporter capability profile."""
    profile = exporter_repo.get_exporter_profile(db)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exporter profile not found.")
    return profile

@router.patch("/profile", response_model=ExporterProfileResponse)
def update_profile(update_data: ExporterProfileUpdate, db: Session = Depends(get_db)):
    """Update profile fields with partial payload."""
    data = update_data.model_dump(exclude_unset=True)
    return exporter_repo.upsert_exporter_profile(db, data)

@router.post("/onboarding/step", response_model=ExporterProfileResponse)
def submit_onboarding_step(req: ExporterOnboardingStepRequest, db: Session = Depends(get_db)):
    """Save-and-resume exporter onboarding wizard step."""
    return exporter_repo.update_onboarding_step(db, step=req.step, step_data=req.data)

@router.get("/readiness-gaps", response_model=ReadinessGapResponse)
def get_readiness_gaps(db: Session = Depends(get_db)):
    """Audit Indian exporter commercial, customs, and regulatory readiness gaps."""
    return exporter_repo.get_readiness_gap_analysis(db)
