# Trade OS — Agent Rules

## Before Any Task
1. Read ai_context/RULES.md
2. Read ai_context/INDEX.md
3. Read ai_context/modules/MODULE_{name}.md for today's module
4. Read ai_context/modules/MODULE_shared.md (always)

## After Any Task
1. Update CODEMAP.json with all new entities
2. Assign TOS-{LAYER}-{MODULE}-{SEQ} codes sequentially
3. Run: python update.py

## Never
- Write a function, route, model, or utility already listed in a MODULE file
- Duplicate logic that exists in another service (scoring, compliance, lane, outreach)
- Write SQL in service files or business logic in repository files
- Insert a match candidate without score + score_version + drivers
- Create a signal without evidence JSONB
- Return raw SQLAlchemy models from API routes

## Architecture Rules (from RULES.md)
1. All DB access → repository layer only. No SQL in services, no logic in repos.
2. All match scoring → scoring_service.py. Never inline in routes.
3. All EUDR/REACH compliance → compliance_service.py. Never duplicate.
4. All lane economics → lane_service.py. No hardcoded freight values.
5. All outreach generation → outreach_service.py.
6. Match candidates require: score + score_version + at least one driver.
7. gold.match_score_history → INSERT ONLY. Never UPDATE or DELETE.
8. audit.audit_event → INSERT ONLY. Never UPDATE or DELETE.
9. Bronze → Silver → Gold data flow only. Never reverse.
10. Every API route except /health requires X-TradeOS-Key header.
11. Pydantic schemas required for all API request/response bodies.
12. Phase 3 (pgvector, agents) must stay in dedicated modules — never pollute Phase 1/2.

## Entity Code Format
TOS-{LAYER}-{MODULE}-{SEQ}
LAYER: DB SVC REP RTE SCH WRK UTL CFG FE INF TST
MODULE: INFRA SCHEMA SEED SCORING API MATCH SIG ACC DATA SEARCH AGENTS SHR
SEQ: 3-digit, zero-padded, per LAYER+MODULE in CODEMAP.json

## Tech Stack
- Backend: FastAPI + Python 3.12 + SQLAlchemy 2.x + PostgreSQL 16
- Schemas: Pydantic v2
- Migrations: Alembic
- Frontend: React 18 + TypeScript + Vite + TanStack Query + Zustand
- Phase 3: pgvector HNSW + LangGraph

## Antigravity 2.0 Command Execution Policy
- **Allowed Development Commands**: `python`, `pytest`, `pip`, `npm`, `npx`, `tsc`, `vite`, `docker compose`, `update.py`, safe non-destructive git commands (`status`, `add`, `commit`, `push origin main`).
- **Prohibited Destructive Commands**: Never run destructive deletions (`rm -rf /`, `rmdir /s /q`), force-pushes (`git push --force`), destructive resets (`git reset --hard` on committed work), volume deletions, or system process kills.
