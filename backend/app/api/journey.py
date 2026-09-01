import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.journey import (
    JourneyStateResponse,
    JourneyTransitionRequest,
    JourneyTransitionResponse,
    StageEventResponse
)
from app.services import journey_service
from app.repositories import journey_repo

router = APIRouter(prefix="/api/v1/journey", tags=["Journey Engine & State Transitions"], dependencies=[Depends(require_api_key)])

@router.get("/opportunities/{opp_id}/state", response_model=JourneyStateResponse)
def get_opportunity_journey_state(opp_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve full journey state, available transitions, blockers, and history for an opportunity."""
    state = journey_service.get_journey_state(db, opp_id)
    if not state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found.")
    return state

@router.post("/opportunities/{opp_id}/transition", response_model=JourneyTransitionResponse)
def execute_opportunity_transition(
    opp_id: uuid.UUID,
    req: JourneyTransitionRequest,
    db: Session = Depends(get_db)
):
    """Execute a backend-validated stage transition with immutable audit logging."""
    try:
        return journey_service.execute_stage_transition(db, opp_id, req)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/opportunities/{opp_id}/history", response_model=List[StageEventResponse])
def get_opportunity_journey_history(opp_id: uuid.UUID, db: Session = Depends(get_db)):
    """Retrieve append-only chronological stage transition events."""
    events = journey_repo.list_stage_events_for_entity(db, "opportunity", opp_id)
    return [StageEventResponse.model_validate(e) for e in events]
