import json
from datetime import datetime, timezone

with open("CODEMAP.json", "r", encoding="utf-8") as f:
    data = json.load(f)

data["meta"]["active_sprint"] = "S3"
data["meta"]["completed_sprints"] = ["S1", "S2", "S3"]
data["modules"]["M10_search"]["status"] = "DONE"
data["modules"]["M11_agents"]["status"] = "DONE"

new_entities = {
    # M10 Search
    "TOS-REP-SEARCH-001": {"name": "search_repo", "file": "backend/app/repositories/search_repo.py", "description": "Sparse full-text & trigram similarity search repository"},
    "TOS-SVC-SEARCH-001": {"name": "HybridSearchEngine / compute_rrf_score", "file": "backend/app/services/search_service.py", "description": "Hybrid pgvector HNSW dense + tsvector sparse Reciprocal Rank Fusion search engine"},
    "TOS-SCH-SEARCH-001": {"name": "HybridSearchRequest / HybridSearchResponse", "file": "backend/app/schemas/search.py", "description": "Pydantic hybrid search request & response models"},
    "TOS-RTE-SEARCH-001": {"name": "hybrid_search", "file": "backend/app/api/search.py", "description": "POST /api/v1/search/hybrid endpoint"},
    "TOS-FE-SEARCH-001": {"name": "api/search.ts", "file": "frontend/src/api/search.ts", "description": "Frontend hybrid search API client"},
    "TOS-TST-SEARCH-001": {"name": "test_hybrid_search.py", "file": "backend/app/tests/test_hybrid_search.py", "description": "Pytest integration tests for RRF math and search endpoint"},

    # M11 Agents
    "TOS-SVC-AGENTS-001": {"name": "ResearchAgent", "file": "backend/app/agents/research_agent.py", "description": "Buyer discovery & decision maker identification agent"},
    "TOS-SVC-AGENTS-002": {"name": "ComplianceAgent", "file": "backend/app/agents/compliance_agent.py", "description": "EUDR 68/100 and REACH chemical compliance gap analysis agent"},
    "TOS-SVC-AGENTS-003": {"name": "NarrativeAgent", "file": "backend/app/agents/narrative_agent.py", "description": "100-point match rationale explanation agent"},
    "TOS-SVC-AGENTS-004": {"name": "OutreachSequenceAgent", "file": "backend/app/agents/outreach_agent.py", "description": "3-step multi-channel export outreach sequence generator"},
    "TOS-SVC-AGENTS-005": {"name": "AccountPlanAgent", "file": "backend/app/agents/account_plan_agent.py", "description": "30-day tactical buyer account plan agent"},
    "TOS-SVC-AGENTS-006": {"name": "MultiAgentOrchestrator", "file": "backend/app/agents/orchestrator.py", "description": "LangGraph multi-agent pipeline orchestrator with human approval gate"},
    "TOS-SCH-AGENTS-001": {"name": "AgentExecutionRequest / AgentWorkflowResponse", "file": "backend/app/schemas/agents.py", "description": "Pydantic agent workflow request and response models"},
    "TOS-RTE-AGENTS-001": {"name": "execute_agent_workflow", "file": "backend/app/api/agents.py", "description": "POST /api/v1/agents/execute endpoint"},
    "TOS-FE-AGENTS-001": {"name": "AgentCockpitCard", "file": "frontend/src/components/accounts/AgentCockpitCard.tsx", "description": "Frontend multi-agent orchestration card & step output viewer"},
    "TOS-FE-AGENTS-002": {"name": "api/agents.ts", "file": "frontend/src/api/agents.ts", "description": "Frontend multi-agent API client"},
    "TOS-TST-AGENTS-001": {"name": "test_agents.py", "file": "backend/app/tests/test_agents.py", "description": "Pytest unit tests for multi-agent workflow state and step execution"}
}

data["entities"].update(new_entities)
data["meta"]["total_entities"] = len(data["entities"])
data["meta"]["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

with open("CODEMAP.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"[SUCCESS] CODEMAP.json updated with {len(data['entities'])} total registered entities across all 11 modules!")
