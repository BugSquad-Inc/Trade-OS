from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AgentExecutionRequest(BaseModel):
    buyer_id: str
    agents: List[str] = ["research", "compliance", "narrative", "outreach", "account_plan"]
    requires_human_approval: bool = True

class AgentStepResult(BaseModel):
    agent_name: str
    status: str
    output: Dict[str, Any]
    execution_time_ms: float

class AgentWorkflowResponse(BaseModel):
    workflow_id: str
    buyer_id: str
    buyer_name: str
    status: str
    completed_steps: List[AgentStepResult]
    approval_required: bool
    summary_action_plan: str
