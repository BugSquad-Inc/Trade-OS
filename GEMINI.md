This project uses a structured codebase memory system in ai_context/.

MANDATORY — before writing any code for any task:
1. Read ai_context/RULES.md
2. Read ai_context/INDEX.md
3. Read ai_context/modules/MODULE_{name}.md for the module in today's task
   (if task touches two modules, read both MODULE files)
   Always also read ai_context/modules/MODULE_shared.md

MANDATORY — after completing any coding task:
1. Update CODEMAP.json with all new entities created
2. Assign the next sequential TOS-{LAYER}-{MODULE}-{SEQ} code to each
3. Run: python update.py

Never write a function, route, model, or utility that already appears
in the MODULE file. If it exists there, call it by its TOS code.
Do not rebuild what already exists.

## Entity Code Format
TOS-{LAYER}-{MODULE}-{SEQ}
Examples: TOS-SVC-SCORING-001, TOS-RTE-API-003, TOS-FE-MATCH-005
Full reference: ai_context/modules/MODULE_shared.md

## Module Files — load only the one for today's task
- MODULE_infra.md     → M1: Docker, FastAPI skeleton, health endpoint, .env
- MODULE_schema.md    → M2: PostgreSQL DDL, bronze/silver/gold/audit schemas, indexes
- MODULE_seed.md      → M3: Butler's Leather + 5 German buyer seed data
- MODULE_scoring.md   → M4: 100-point scoring engine, ScoreDriver, MatchScore
- MODULE_api.md       → M5: FastAPI routes, Pydantic schemas, repositories
- MODULE_match_ui.md  → M6: React Match Portal, ExporterCapabilityCard, MatchCard
- MODULE_signals_ui.md → M7: Live Signals Feed, EUDR Scorecard, REACH Scorecard
- MODULE_account_ui.md → M8: Account 360 tabs, OutreachComposer
- MODULE_data_expand.md → M9: Phase 2 multi-source ingestion
- MODULE_search.md    → M10: Phase 3 pgvector hybrid search
- MODULE_agents.md    → M11: Phase 3 LangGraph agents
- MODULE_shared.md    → Shared utilities — ALWAYS load alongside any module

## Antigravity 2.0 Command Execution Policy
- **Allowed Development Commands**: `python`, `pytest`, `pip`, `npm`, `npx`, `tsc`, `vite`, `docker compose`, `update.py`, safe git operations (`git status`, `git add`, `git commit`, `git push origin main`).
- **Prohibited Destructive Commands**: Never run destructive deletions (`rm -rf /`, `rmdir /s /q`), force-pushes (`git push --force`), destructive resets (`git reset --hard` on committed work), volume deletions, or system process kills.
