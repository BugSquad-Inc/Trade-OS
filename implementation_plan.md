# Trade OS — End-to-End Implementation Plan

> **Product:** Export Revenue Operating System — Leather & Materials Vertical  
> **Wedge:** Butler's Leather Chennai → German/EU Buyers  
> **Frontend Design System:** Apple Human Interface Guidelines ([Apple Design](https://developer.apple.com/design/))  
> **Schema Convention:** Enterprise — `silver.entity_company`, `gold.match_candidate` ([architecture spec](docs/trade_os_architecture_and_sprint_plan.md))  
> **Scoring Formula:** 35/25/15/15/10 (5 drivers: Product Fit, Compliance, Lane Economics, Intent Signals, Accessibility)  
> **Revenue Target:** $500 paid pilot in 8 days → $2,500/month enterprise in 3 months

---

## What Was Built (ai_context System)

The `ai_context/` system is now live. Every AI coding session starts by reading ~850 tokens of context instead of re-learning the entire codebase. The system consists of:

| File | Purpose | Tokens |
|------|---------|--------|
| `GEMINI.md` | Auto-loaded by Antigravity every session | ~150 |
| `AGENTS.md` | Cross-tool rules (Cursor, Claude Code, Codex) | ~250 |
| `CODEMAP.json` | Source of truth — you and AI update this | machine |
| `update.py` | Regenerates all MODULE files from CODEMAP | tool |
| `post-commit` | Git hook: auto-runs update.py on every commit | auto |
| `ai_context/RULES.md` | 15 architectural laws — always loaded | ~150 |
| `ai_context/INDEX.md` | Module status board — always loaded | ~300 |
| `ai_context/modules/` | 12 module files — load only today's | ~400 each |

**One-time setup** (run once):
```bash
cp post-commit .git/hooks/post-commit
chmod +x .git/hooks/post-commit  # (on Linux/macOS only)
python update.py --check
python update.py
```

---

## Canonical Decisions (from Validated Audit)

> **Scoring Formula (canonical):** `score_product_fit(35) + score_compliance(25) + score_lane_economics(15) + score_intent_signals(15) + score_accessibility(10) = 100`  
> *Note: `butlers_mvp_react_postgres_execution.md` uses 40/30/20/10 and `butlers_leather_prototype_and_demo_plan.md` uses 30/25/15/10/20. Both are superseded by this plan.*

> **Schema Vocabulary (canonical):** Enterprise naming from `trade_os_architecture_and_sprint_plan.md`:  
> - Companies → `silver.entity_company` (not `silver.accounts` or `silver.buyers`)  
> - Match candidates → `gold.match_candidate` (not `gold.match_scores`)  
> - Score history → `gold.match_score_history` (INSERT ONLY)  
> - Audit log → `audit.audit_event` (INSERT ONLY)  
> - Contacts → `silver.entity_person` with `confidence` field  
> - Freight → `silver.trade_lane_benchmark`  
> - Exporter profiles → `gold.exporter_capability`  

> **EUDR Readiness Score (canonical):** Butler's Leather = **68/100**  
> *Note: `butlers_mvp_react_postgres_execution.md` line 867 shows 58. That is superseded.*

> **GDPR Compliance:** All seeded EU contacts must include `consent_status: 'legitimate_interest'` and `legal_basis: 'B2B legitimate interest under GDPR Art. 6(1)(f)'`. UI must display a visible disclaimer: *"Contact roles sourced from public directories — verify before direct outreach."*

---

## Phase 1 — Sprint 1 (Days 1–8): $500 Pilot MVP

### Day 1 — M1: Infrastructure

**Goal:** Working dev environment

**Files to create:**
- `docker-compose.yml` — PostgreSQL 16 + FastAPI containers
- `backend/Dockerfile`
- `.env.example`
- `Makefile`
- `backend/app/main.py` — FastAPI + CORS
- `backend/app/config.py` — settings from env
- `backend/app/database.py` — SQLAlchemy engine + get_db
- `backend/app/api/deps.py` — require_api_key
- `backend/app/api/health.py` — GET /api/v1/health
- `backend/app/schemas/health.py`
- `backend/app/tests/test_health.py`

**Exit:** `curl http://localhost:8000/api/v1/health` → `{"status": "ok"}`

---

### Day 2 — M2 + M3: Schema + ORM Models + Seed Data

**Goal:** PostgreSQL medallion DDL + SQLAlchemy 2.x ORM models + Butler's Leather + 5 German buyers seeded

**DDL Files to create:**
- `backend/sql/001_extensions.sql` → pgcrypto, pg_trgm, vector
- `backend/sql/002_schemas.sql` → bronze/silver/gold/audit
- `backend/sql/003_functions.sql` → set_updated_at, notify_match_refresh
- `backend/sql/004_bronze.sql` → bronze.source_system, bronze.raw_document, bronze.raw_extract, bronze.raw_event + 4 more
- `backend/sql/005_silver.sql` → silver.entity_company, silver.entity_person, silver.entity_product, silver.entity_certification, silver.entity_relationship, silver.entity_document + search_vector columns
- `backend/sql/006_gold.sql` → gold.match_candidate, gold.match_score_history (INSERT ONLY), gold.signal, gold.signal_evidence, gold.exporter_capability, gold.match_profile, audit.audit_event (INSERT ONLY)
- `backend/sql/007_indexes.sql` → GIN, trgm, btree, HNSW indexes
- `backend/sql/008_triggers.sql` → updated_at + match_refresh triggers

**SQLAlchemy ORM Models (maps to DDL above):**
- `backend/app/models/__init__.py`
- `backend/app/models/base.py` — DeclarativeBase, schema-aware metadata for bronze/silver/gold/audit
- `backend/app/models/company.py` — `EntityCompany` (silver.entity_company), `EntityPerson` (silver.entity_person)
- `backend/app/models/match.py` — `MatchCandidate` (gold.match_candidate), `MatchScoreHistory` (gold.match_score_history)
- `backend/app/models/signal.py` — `Signal` (gold.signal), `SignalEvidence` (gold.signal_evidence)
- `backend/app/models/compliance.py` — `EntityCertification` (silver.entity_certification)
- `backend/app/models/lane.py` — `TradeLaneBenchmark` (silver.trade_lane_benchmark)
- `backend/app/models/exporter.py` — `ExporterCapability` (gold.exporter_capability)

**Seed Script:**
- `backend/app/scripts/seed_db.py` → Butler's Leather exporter + 5 German buyers (*Picard, Roeckl, Bader, Kilger, Otto Schumacher*) + freight lane benchmarks (*Chennai INMAA → Hamburg DEHAM*)
  - All seeded contacts include `confidence` score (Rule 10)
  - All seeded contacts include `consent_status: 'legitimate_interest'` + `legal_basis: 'B2B legitimate interest under GDPR Art. 6(1)(f)'`
  - All seeded contacts flagged with `verification_status: 'illustrative'`
  - All signals include `evidence` JSONB (Rule 9)
  - All lane benchmarks include `effective_start` date (Rule 11)
  - Butler's EUDR readiness score: **68/100** (canonical)

**Exit criteria:**
```sql
SELECT count(*) FROM silver.entity_company;          -- 6 (1 exporter + 5 buyers)
SELECT count(*) FROM gold.exporter_capability;       -- 1 (Butler's Leather)
SELECT count(*) FROM silver.trade_lane_benchmark;    -- 1 (Chennai → Hamburg)
SELECT count(*) FROM silver.entity_person;           -- 5+ (buyer contacts with confidence scores)
```

---

### Day 3 — M4: Scoring Engine

**Goal:** 100-point explainable match scoring (canonical formula: 35/25/15/15/10)

**Files to create:**
- `backend/app/services/scoring_service.py`
  - `score_product_fit()` → 35 pts (material match, tannage/finish, HS code overlap, thickness range)
  - `score_compliance()` → 25 pts (EUDR readiness alignment, REACH/LWG certification overlap)
  - `score_lane_economics()` → 15 pts (route viability, incoterm alignment, freight benchmark)
  - `score_intent_signals()` → 15 pts (recency-decayed buyer activity, sustainability language, hiring signals)
  - `score_accessibility()` → 10 pts (contactability, procurement transparency, verified buyer contacts)
  - `score_match()` → MatchScore with 5 ScoreDriver objects + human-readable evidence strings
  - `grade_from_score()` → Grade A (≥85), B (≥70), C (≥55), D (<55)
- `backend/app/repositories/match_repo.py`
  - `upsert_match_candidate()` → requires score + score_version + ≥1 driver (Rule 6)
  - `insert_score_history()` ← INSERT ONLY into gold.match_score_history (Rule 7)
- `backend/app/scripts/run_scoring.py`
- `backend/app/tests/test_scoring.py`

**Exit:** 5 matches scored, each with grade + 5 driver objects + evidence strings

---

### Day 4 — M5: FastAPI REST API

**Goal:** All routes returning valid JSON via Pydantic schemas (Rule 13)

**Files to create:**
- `backend/app/schemas/` — match.py, signal.py, account.py, outreach.py, capability.py
- `backend/app/api/` — matches.py, signals.py, accounts.py, outreach.py, capability.py
- `backend/app/services/` — match_service.py, outreach_service.py, compliance_service.py, lane_service.py
- `backend/app/repositories/` — account_repo.py, signal_repo.py, outreach_repo.py, capability_repo.py
- `backend/app/tests/` — test_matches.py, test_signals.py, test_accounts.py, test_outreach.py, test_capability.py

**Routes:**
```
GET  /api/v1/health              (no auth)
GET  /api/v1/capability          (X-TradeOS-Key required) ← powers ExporterProfileCard
GET  /api/v1/matches             (X-TradeOS-Key required)
GET  /api/v1/signals             (X-TradeOS-Key required)
GET  /api/v1/accounts/{id}       (X-TradeOS-Key required)
POST /api/v1/outreach            (X-TradeOS-Key required)
```

**Exit:** All routes tested with curl + pytest

---

### Day 5a — M6 Part 1: Apple HIG Design System + Layout Shell

**Goal:** Reusable Apple-grade design system and macOS Pro App Shell.

#### 5a.1 Design System & Foundations ([developer.apple.com/design](https://developer.apple.com/design/))
- **Typography (cross-platform safe):**
  - Primary: `Inter` (open-source, metrically closest to SF Pro) loaded via `@font-face` from CDN
  - Apple override: `-apple-system, BlinkMacSystemFont` renders native SF Pro on macOS/iOS
  - Full stack: `'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif`
  - Monospace: `'JetBrains Mono', 'SF Mono', ui-monospace, Menlo, Consolas, monospace`
  - Type scale: Large titles (`text-3xl font-bold tracking-tight`), body (`text-sm leading-relaxed`), captions (`text-[11px] font-medium tracking-wide uppercase`), tabular numbers (`font-mono tabular-nums`) for scores, currency, HS codes
- **Materials & Vibrancy:**
  - Ultra-thin / Thin / Regular / Thick glassmorphism using `backdrop-blur-xl`
  - Light mode: `bg-white/80 border-black/[0.06] shadow-sm`
  - Dark mode: `bg-zinc-900/80 border-white/[0.08] shadow-md`
  - Surface hierarchy: `bg-systemBackground` (canvas) → `bg-secondarySystemBackground` (cards) → `bg-tertiarySystemBackground` (elevated popovers & sheets)
- **Semantic Palette:**
  - System Blue (`#007AFF`), Green (`#34C759`), Orange (`#FF9500`), Red (`#FF3B30`), Indigo (`#5856D6`), Purple (`#AF52DE`), Teal (`#30B0C7`)
- **Motion & Interaction:**
  - Physics-based spring: `framer-motion` (`{ type: "spring", stiffness: 400, damping: 30 }`)
  - Layout morphing via `layoutId` on segmented pill controls
  - Tactile micro-interactions: `whileTap={{ scale: 0.98 }}`

#### 5a.2 Files to Create:
- `frontend/package.json` — Vite + React 18 + TypeScript + Tailwind CSS + Framer Motion + Lucide React + TanStack Query + Zustand
- `frontend/src/index.css` — `@font-face` for Inter, global Tailwind config
- `frontend/src/theme/appleTokens.ts` — Apple HIG design tokens (typography, colors, materials, shadows, radii)
- `frontend/src/components/apple/` — Core Apple HIG UI Primitives:
  - `AppleSegmentedControl.tsx` (TOS-FE-SHR-001): Pill switcher with animated sliding background capsule
  - `AppleScoreRing.tsx` (TOS-FE-SHR-002): WatchOS Activity Ring concentric circular SVG progress gauge with grade badge
  - `AppleCard.tsx` (TOS-FE-SHR-003): Inset squircle card (`rounded-2xl`) with hairline specular border
  - `AppleBadge.tsx` (TOS-FE-SHR-004): Semantic status pill with soft translucent fill
  - `AppleButton.tsx` (TOS-FE-SHR-005): Spring-animated button (Primary, Secondary, Glass, Destructive)
  - `AppleDrawer.tsx` (TOS-FE-SHR-006): macOS Quick Look / Inspector slide-over detail sheet
  - `AppleCommandBar.tsx` (TOS-FE-SHR-007): Spotlight `Cmd+K` keyboard command palette
  - `AppleGauge.tsx` (TOS-FE-SHR-008): Linear bar gauge with semantic color gradient
- `frontend/src/components/layout/` — macOS Pro App Shell:
  - `AppShell.tsx`: 3-column split view (Translucent Sidebar, Main Feed, Slide-over Inspector)
  - `GlassSidebar.tsx`: Frosted glass navigation with categorized items, active capsule indicator, and live count badges
  - `GlassTopbar.tsx`: Header bar with breadcrumbs, live sync status pill, search trigger, and dark/light toggle
  - `ViewHeader.tsx`: Apple large-title page header with primary action buttons
- `frontend/src/components/ui/` — Error & Loading States:
  - `PageSkeleton.tsx` (TOS-FE-SHR-009): Shimmer loading skeleton for all views
  - `ErrorBoundary.tsx` (TOS-FE-SHR-010): Graceful error boundary with retry action
  - `EmptyState.tsx` (TOS-FE-SHR-011): Empty state placeholder with illustration and CTA

**Exit Criteria:** Design system renders correctly on both macOS (SF Pro) and Windows (Inter fallback). All primitives demo-ready in a Storybook-style test page. Dark/light mode toggle works.

---

### Day 5b — M6 Part 2: Match Portal UI

**Goal:** Match Portal rendering from live API using Day 5a design system.

**Files to create:**
- `frontend/src/components/matches/` — Match Portal Components:
  - `MatchPortalView.tsx` (TOS-FE-MATCH-001): Main screen view combining exporter capability and ranked buyer cards
  - `ExporterProfileCard.tsx` (TOS-FE-MATCH-002): Butler's Leather factory capability badge (data from `GET /api/v1/capability`)
  - `MatchCard.tsx` (TOS-FE-MATCH-003): Ranked German buyer card with `AppleScoreRing`, 5 driver pills, and next best action
  - `MatchDriverBadge.tsx` (TOS-FE-MATCH-004): Individual driver badge with points and tooltip evidence
  - `MatchFilterBar.tsx` (TOS-FE-MATCH-005): Segmented pill controls for Match Grade (A/B/C), Country, and Product Category
  - `MatchInspector.tsx` (TOS-FE-MATCH-006): Slide-over inspector sheet showing deep score breakdown and evidence source
  - `MatchPortalSkeleton.tsx` (TOS-FE-MATCH-007): Loading shimmer state for match portal
- `frontend/src/api/client.ts` — Axios/fetch client with `X-TradeOS-Key` header
- `frontend/src/api/matches.ts` & `frontend/src/api/capability.ts` — TanStack Query API clients
- `frontend/src/hooks/useMatches.ts` & `frontend/src/hooks/useCapability.ts`
- `frontend/src/store/uiStore.ts` — Zustand store (selected match, active drawer, theme)

**Exit Criteria:** Match Portal loads with Apple HIG aesthetics, shows Butler's Leather card + 5 ranked German buyer matches with animated score rings, driver badges, next best actions, slide-over inspector, and loading/error states.

---

### Day 6 — M7: Signals Feed + Compliance UI (Apple HIG)

**Goal:** Live Signals Feed, EUDR/REACH Compliance Audit dashboards.

#### 6.1 Screen 2: Live Signals & Compliance Feed (M7)
- `frontend/src/components/signals/`
  - `SignalsView.tsx` (TOS-FE-SIG-001): Grid view orchestrating EUDR scorecard, freight benchmarks, and live event feed
  - `EUDRScorecard.tsx` (TOS-FE-SIG-002): **68/100** Readiness audit matrix with interactive gap checklist (geolocation polygon, due diligence statement, deforestation-free certification)
  - `REACHComplianceCard.tsx` (TOS-FE-SIG-003): SVHC substance test matrix with safety declarations and test lab verification status
  - `FreightLaneWidget.tsx` (TOS-FE-SIG-004): Chennai (INMAA) → Hamburg (DEHAM) ocean transit benchmark (26-34 days, \$1,850/FEU ocean rate, port congestion index)
  - `SignalFeedItem.tsx` (TOS-FE-SIG-005): Real-time event cards with urgency pills (Critical, High, Medium), source quote snippet, timestamp, and action buttons
  - `SignalFilterPills.tsx` (TOS-FE-SIG-006): Category filter pills (Tenders, Regulatory, Supply Chain, Executive Hiring, M&A)
  - `SignalsSkeleton.tsx` (TOS-FE-SIG-007): Loading shimmer state for signals view
- `frontend/src/api/signals.ts` & `frontend/src/hooks/useSignals.ts`

**Exit Criteria:** Signals view renders EUDR scorecard (68/100), freight benchmarks, and signal feed with loading states.

---

### Day 7 — M8: Account 360 + Outreach (Apple HIG)

**Goal:** Account 360 Decision Cockpit with AI outreach + Spotlight navigation.

#### 7.1 Screen 3: Account 360 & AI Outreach Cockpit (M8)
- `frontend/src/components/accounts/`
  - `Account360View.tsx` (TOS-FE-ACC-001): Deep intelligence dossier container for German buyers
  - `AccountHeader.tsx` (TOS-FE-ACC-002): Buyer identity dossier banner (Picard GmbH, Roeckl, Bader, etc.) with location, procurement volume, and verification badge (🟢 Verified / 🟡 Inferred / 🔴 Illustrative)
  - `AccountTabs.tsx` (TOS-FE-ACC-003): `AppleSegmentedControl` switching between deep intelligence tabs
  - `TabOverview.tsx` (TOS-FE-ACC-004): Buyer profile, purchase volume, product requirements, and catalog overlap analysis
  - `TabCompliance.tsx` (TOS-FE-ACC-005): Full EUDR geofencing & REACH chemical testing requirements breakdown
  - `TabLaneEconomics.tsx` (TOS-FE-ACC-006): Landed cost calculator, tariff benchmarks, and container economics
  - `TabContacts.tsx` (TOS-FE-ACC-007): Procurement contacts with confidence scores, LinkedIn links, and GDPR disclaimer banner: *"Contact roles sourced from public directories — verify before direct outreach."*
  - `OutreachComposer.tsx` (TOS-FE-ACC-008): macOS Mail-style AI message composer with tone switcher (Professional, Direct, Technical, Relationship), personalized value props, live preview, and 1-click clipboard / mailto / CRM export
  - `AccountSkeleton.tsx` (TOS-FE-ACC-009): Loading shimmer state for account 360
- `frontend/src/api/accounts.ts` & `frontend/src/hooks/useAccount.ts`

#### 7.2 Global Spotlight & Keyboard Navigation
- `AppleCommandBar.tsx` wired globally with `Cmd+K` / `Ctrl+K`:
  - Rapid search across all 5 German buyers, HS codes (`4107`, `4104`), EUDR articles, and live signals
  - Keyboard shortcuts: `1` (Match Portal), `2` (Signals Feed), `3` (Account 360), `Esc` (Close Drawer/Modal)

**Exit Criteria:** Account 360 and Outreach Composer demo-ready, contact cards show verification badges and GDPR disclaimer, smooth 60fps spring transitions, dark/light mode parity.

---

### Day 8 — Demo Dry Run

**Goal:** Rehearse and close $500 pilot

**Checklist:**
- [ ] All 3 views load without errors with Apple HIG visual polish (Inter font on Windows, SF Pro on macOS)
- [ ] 5 buyer matches with explainable scores (35/25/15/15/10 formula) + driver pills
- [ ] EUDR scorecard renders (score: 68/100 readiness gap — canonical value)
- [ ] Chennai-Hamburg freight metrics benchmarked (from silver.trade_lane_benchmark)
- [ ] Outreach composer generates personalized German buyer message
- [ ] Contact cards show verification badges and GDPR disclaimer
- [ ] Loading skeletons render during API calls; error boundaries catch failures gracefully
- [ ] Demo narrative under 15 minutes
- [ ] Pilot agreement ready (14-day, 5 qualified matches, $500 refund guarantee)
- [ ] Payment link ready

---

## Phase 2 — Weeks 2–4: Expand to 3–5 Design Partners

### M9: Data Expansion
- Add bronze ingestion scripts for 3+ source types
- Entity resolution service (dedup_key matching)
- Expand from 6 seed accounts to 50+ accounts
- 100+ signals generated
- Nightly refresh worker

### Commercial
- 3–5 pilots × $500–$750 = $1,500–$3,750
- Chemical distributor module (REACH-compliance opportunities)
- Machinery vendor module (capacity expansion signals)
- Weekly rhythm: data refresh Monday, partner review Tuesday, outreach Wednesday

---

## Phase 3 — Months 2–3: Enterprise $2,500/month

### M10: Hybrid Search
- pgvector HNSW semantic search (text-embedding-3-small)
- tsvector BM25-like full-text on silver.entity_company + silver.entity_product
- Reciprocal Rank Fusion endpoint
- Natural language queries: "Find German buyers of bovine leather for automotive"

### M11: LangGraph Agents
- Research Agent — account discovery + contact identification
- Compliance Agent — EUDR/REACH gap scorecard generation
- Match Explanation Agent — human-readable match narratives
- Outreach Agent — personalized email + LinkedIn sequences
- Account Planning Agent — 30-day account plans
- Human approval gate before any external action

### Enterprise Tier: $2,500/month
- 5 seats, 500 accounts monitored
- Daily match refresh
- Customs BOL flows
- Weekly lane benchmark refresh
- CRM export (CSV first, HubSpot later)
- Agent workflow pack

---

## ai_context Daily Workflow

```
MORNING: Antigravity auto-reads GEMINI.md → RULES.md + INDEX.md load
TASK:    Tell Antigravity which module (e.g., "Work on M4 scoring engine")
         → Loads MODULE_scoring.md automatically (or read it manually)
CODING:  Agent references TOS codes for existing functions
         Never recreates what already exists
END:     Type /codemap-update
         Agent updates CODEMAP.json + runs update.py
COMMIT:  git commit → post-commit hook → ai_context files auto-amended
```

---

## Entity Code Format Quick Reference

```
TOS-{LAYER}-{MODULE}-{SEQ}

Examples:
  TOS-DB-SCHEMA-008    silver.entity_company table
  TOS-SVC-SCORING-007  score_match() function
  TOS-RTE-API-002      GET /api/v1/matches
  TOS-FE-MATCH-005     MatchScoreRing component
  TOS-UTL-SHR-001      require_api_key shared dependency
```

To find next SEQ: check CODEMAP.json → filter by LAYER+MODULE → take max SEQ + 1.

---

## Open Questions

> [!IMPORTANT]
> **Q1: Butler's Leather contact info** — Do you have the actual Butler's Leather contact to schedule the Day 8 demo call? The seed data uses placeholder contacts. Real contacts need to be verified before external outreach.

> [!IMPORTANT]  
> **Q2: Docker environment** — Is Docker Desktop installed and running on this machine? Day 1 requires it.

> [!NOTE]
> **Q3: Frontend framework** — The plan specifies React 18 + Vite. Should we initialize the frontend project now, or do you want to focus on the backend first?

> [!NOTE]
> **Q4: German buyer data accuracy** — The 5 buyer dossiers (Picard, Roeckl, Bader, Kilger, Otto Schumacher) use placeholder/public-source data. Before any external outreach, each buyer profile needs verification. The seed script already flags this with `verification_status: public_source_placeholder`.
