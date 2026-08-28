from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class AgentWorkflowState(BaseModel):
    workflow_id: str
    buyer_id: str
    buyer_name: str
    company_data: Dict[str, Any] = {}
    exporter_data: Dict[str, Any] = {}
    research_summary: Dict[str, Any] = {}
    compliance_audit: Dict[str, Any] = {}
    match_narrative: str = ""
    outreach_sequence: List[Dict[str, Any]] = []
    account_plan_30d: List[Dict[str, Any]] = []
    approval_granted: bool = False
    status: str = "running"
