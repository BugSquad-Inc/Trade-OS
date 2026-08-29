import uuid
from datetime import datetime, date
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.deal import TodayCockpitResponse, TaskItemResponse
from app.repositories import deal_repo, exporter_repo

router = APIRouter(prefix="/api/v1/today", tags=["Today Cockpit"], dependencies=[Depends(require_api_key)])

@router.get("", response_model=TodayCockpitResponse)
def get_today_cockpit(db: Session = Depends(get_db)):
    """Executive morning dashboard consolidating urgent tasks, pipeline velocity, and recommended actions."""
    profile = exporter_repo.get_exporter_profile(db)
    exporter_name = profile.company_name if profile else "Butler's Leather"
    readiness_score = profile.eudr_readiness_score if profile else 95

    tasks = deal_repo.list_today_tasks(db, status_filter="todo")
    pipeline = deal_repo.get_pipeline_summary(db)

    recommended_actions = [
        {
            "priority": "URGENT",
            "type": "outreach_approval",
            "title": "Review & Dispatch Sample Swatch Pack to Picard GmbH",
            "description": "Johann Schmidt requested AW26 calfskin full-grain sample after LWG Gold audit clearance.",
            "target": "Picard GmbH",
            "est_deal_value_eur": 45000
        },
        {
            "priority": "HIGH",
            "type": "quote_followup",
            "title": "Confirm Landed DDP Quote for Roeckl Handschuhe",
            "description": "5,000 sqft kid nappa quotation €17,750 sent. Follow up on custom tannage approval.",
            "target": "Roeckl Handschuhe",
            "est_deal_value_eur": 17750
        },
        {
            "priority": "MEDIUM",
            "type": "dds_verification",
            "title": "Generate Digital Product Passport QR for Bader Auto Batch",
            "description": "Batch 4104 wet-blue crust requires updated Chromium VI certificate before shipment dispatch.",
            "target": "Bader GmbH",
            "est_deal_value_eur": 120000
        }
    ]

    return TodayCockpitResponse(
        date=datetime.now().strftime("%A, %B %d, %Y"),
        exporter_name=exporter_name,
        readiness_score=readiness_score,
        urgent_tasks=tasks,
        pipeline_summary=pipeline,
        recommended_actions=recommended_actions
    )

@router.post("/tasks/{task_id}/complete", response_model=TaskItemResponse)
def mark_task_complete(task_id: uuid.UUID, db: Session = Depends(get_db)):
    """Mark an executive action task as completed."""
    task = deal_repo.complete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task item not found.")
    return task
