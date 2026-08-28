from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.api.deps import require_api_key
from app.schemas.agents import AgentExecutionRequest, AgentWorkflowResponse
from app.agents.orchestrator import MultiAgentOrchestrator

router = APIRouter(prefix="/api/v1/agents", tags=["LangGraph Multi-Agents"])

@router.post("/execute", response_model=AgentWorkflowResponse)
def execute_agent_workflow(
    req: AgentExecutionRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    try:
        b_uuid = uuid.UUID(req.buyer_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid buyer UUID format")

    try:
        res = MultiAgentOrchestrator.execute_workflow(db, b_uuid)
        return AgentWorkflowResponse(**res)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
