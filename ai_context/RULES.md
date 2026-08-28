# Trade OS — Architectural Rules

1. All database access goes through the repository layer; no raw SQL in service files, no business logic in repository files.
2. All scoring goes through `scoring_service.py`; never compute match scores inline in routes or repositories.
3. All compliance scoring (EUDR, REACH) goes through `compliance_service.py`; never bypass or duplicate compliance logic.
4. All lane economics data goes through `lane_service.py`; never hardcode freight benchmarks in routes or components.
5. All outreach message generation goes through `outreach_service.py`; never generate messages directly in API routes.
6. All match candidates must have score, score_version, and at least one driver object; never insert a match without explainability.
7. `gold.match_score_history` is INSERT ONLY — never UPDATE or DELETE score history records.
8. `audit.audit_event` is INSERT ONLY — never UPDATE or DELETE audit records.
9. Every signal must have evidence JSONB; never create a signal with empty evidence.
10. Every contact must have a confidence_score; never insert a contact without a confidence value.
11. Every lane benchmark must have an effective_start date; never insert a benchmark without dating it.
12. Bronze → Silver → Gold data flow is one-directional; never write from Gold back to Silver or Bronze.
13. API routes must use Pydantic schemas for all request and response bodies; never return raw SQLAlchemy model objects.
14. Every API route (except `/health`) must require the `X-TradeOS-Key` header via the `require_api_key` dependency.
15. Phase 3 features (pgvector, LangGraph agents) must not pollute Phase 1/2 service or repository code; keep them in dedicated modules.
