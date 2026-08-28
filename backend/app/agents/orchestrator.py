import uuid
import time
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.repositories import account_repo, capability_repo, match_repo
from app.agents.research_agent import ResearchAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.narrative_agent import NarrativeAgent
from app.agents.outreach_agent import OutreachSequenceAgent
from app.agents.account_plan_agent import AccountPlanAgent

class MultiAgentOrchestrator:
    """Executes multi-agent workflow with human-in-the-loop approval gate."""
    @staticmethod
    def execute_workflow(db: Session, buyer_id: uuid.UUID) -> Dict[str, Any]:
        company = account_repo.get_company_by_id(db, buyer_id)
        if not company:
            raise ValueError(f"Company {buyer_id} not found")

        exporter = capability_repo.get_exporter_capability(db)
        match = match_repo.get_match_by_buyer_id(db, buyer_id)
        match_score = float(match.total_score) if match else 85.0

        workflow_id = str(uuid.uuid4())
        steps = []

        # 1. Research Agent
        t0 = time.time()
        res_output = ResearchAgent.run(company)
        steps.append({"agent_name": "ResearchAgent", "status": "completed", "output": res_output, "execution_time_ms": round((time.time() - t0) * 1000, 2)})

        # 2. Compliance Agent
        t0 = time.time()
        comp_output = ComplianceAgent.run(company, exporter)
        steps.append({"agent_name": "ComplianceAgent", "status": "completed", "output": comp_output, "execution_time_ms": round((time.time() - t0) * 1000, 2)})

        # 3. Narrative Agent
        t0 = time.time()
        narrative_output = NarrativeAgent.run(company, exporter, match_score)
        steps.append({"agent_name": "NarrativeAgent", "status": "completed", "output": {"narrative": narrative_output}, "execution_time_ms": round((time.time() - t0) * 1000, 2)})

        # 4. Outreach Sequence Agent
        t0 = time.time()
        outreach_seq = OutreachSequenceAgent.run(company, exporter)
        steps.append({"agent_name": "OutreachSequenceAgent", "status": "completed", "output": {"sequence": outreach_seq}, "execution_time_ms": round((time.time() - t0) * 1000, 2)})

        # 5. Account Plan Agent
        t0 = time.time()
        plan_output = AccountPlanAgent.run(company)
        steps.append({"agent_name": "AccountPlanAgent", "status": "completed", "output": {"plan_30d": plan_output}, "execution_time_ms": round((time.time() - t0) * 1000, 2)})

        return {
            "workflow_id": workflow_id,
            "buyer_id": str(buyer_id),
            "buyer_name": company.canonical_name,
            "status": "completed_pending_approval",
            "completed_steps": steps,
            "approval_required": True,
            "summary_action_plan": f"Generated 30-day tactical plan & 3-step outreach sequence for {company.canonical_name}."
        }
