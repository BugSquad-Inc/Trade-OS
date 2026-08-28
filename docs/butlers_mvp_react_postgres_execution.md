

# Butler’s Leather Trade OS MVP: 7–10 Day Execution Masterclass

## 1. Architecture & Scope Validation

### Short answer: Yes — but only if you build a lean Postgres-native Medallion monolith, not a big-data science platform.

For the Butler’s Leather MVP, **React + FastAPI + PostgreSQL + pgvector is the right stack**, provided you treat the Medallion architecture as a **simple logical data pattern inside Postgres**, not as a full Spark/Databricks/Airflow-style platform.

Your MVP should feel like a **revenue-generation cockpit**, not a data engineering demo.

---

## MVP Architecture Guardrails

Use this architecture:

```text
React Frontend
  Vite + Tailwind + shadcn/ui
  TanStack Query
  React Router

FastAPI Backend
  Pydantic models
  Read-only match/signal endpoints
  Action endpoint for outreach generation

PostgreSQL
  bronze schema: raw JSONB imports
  silver schema: cleaned canonical entities
  gold schema: match scores, account 360, actions
  pgvector installed but not on critical path
```

### Do not build:

- Kafka
- Airflow
- Spark
- microservices
- event streaming
- vector-search-first matching
- multi-tenant SaaS auth
- billing
- CRM native integration
- real-time scraping
- notification engine
- mobile app
- admin CRUD
- complex permissions

For the next 7–10 days, your job is to prove one thing:

> Trade OS can help Butler’s Leather identify, prioritize, and contact the right European leather buyers faster than they can manually.

That is the only thing that matters.

---

# 2. Lean Medallion Flow for Butler’s Leather

Use Medallion as three Postgres schemas:

```sql
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
```

The MVP pipeline should be:

```text
Manual CSV / JSON / research
        ↓
Bronze: raw immutable records
        ↓
Silver: cleaned buyer, capability, compliance, signal tables
        ↓
Gold: match scores, account 360, recommended actions
        ↓
FastAPI
        ↓
React UI
```

No orchestration tool. Use Python scripts and a Makefile.

Example:

```bash
make seed-bronze
make transform-silver
make score-gold
make api
make web
```

---

## Bronze Layer: Store Raw Evidence

Bronze should be raw, source-linked, and immutable.

### Bronze tables

```text
bronze.raw_buyers
bronze.raw_signals
bronze.raw_capabilities
bronze.raw_freight_benchmarks
```

### `bronze.raw_buyers`

Use this for European buyer research.

```text
id
source_name
source_url
payload JSONB
loaded_at
ingestion_method
source_confidence
```

Example payload:

```json
{
  "company_name": "Picard",
  "country": "Germany",
  "website": "https://www.picard.de",
  "segment": "Leather goods / accessories",
  "product_categories": ["bags", "small leather goods"],
  "procurement_notes": "Public emphasis on quality leather and sustainability.",
  "eudr_signal": "Mentions responsible sourcing.",
  "import_region_interest": ["Asia", "India"],
  "contact_hint": "Procurement page / trade fair presence"
}
```

For the MVP, seed buyers like:

- Picard
- Roeckl
- Bader
- Kilger
- Otto Schumacher

But do not treat these as confirmed matches automatically. Each buyer must pass a hard filter:

> Does this company plausibly buy leather, leather components, or leather goods from non-EU suppliers?

If not, exclude it from the match list.

---

### `bronze.raw_signals`

Store trade news, EUDR-related evidence, procurement signals, freight signals, and buyer activity.

```text
id
source_name
source_url
payload JSONB
loaded_at
signal_type
source_confidence
```

Example:

```json
{
  "signal_type": "eudr",
  "entity": "European leather goods buyer",
  "headline": "Buyer sustainability report references traceability and deforestation-free supply chains.",
  "date": "2025-11-15",
  "impact": "Increases urgency for EUDR-ready leather suppliers.",
  "source_url": "https://example.com/report"
}
```

Important: do not claim official EUDR filings unless you have verified public evidence. For MVP, label these as:

```text
inferred_signal
public_claim
manual_research
regulatory_context
```

---

### `bronze.raw_capabilities`

Store Butler’s Leather capability data as raw JSON.

Example:

```json
{
  "company_name": "Butler's Leather",
  "location": "Chennai, India",
  "export_market_focus": ["Germany", "EU"],
  "material_types": ["finished leather", "leather for goods"],
  "tannage": ["vegetable", "chrome", "chrome-free"],
  "thickness_range_mm": ["0.8", "1.0", "1.2", "1.4"],
  "finish_capabilities": ["aniline", "semi-aniline", "pigmented"],
  "monthly_capacity_sqft": 50000,
  "moq_sqft": 3000,
  "lead_time_days": 30,
  "port_of_export": "Chennai",
  "incoterms": ["FOB", "CIF", "EXW"],
  "certifications": ["LWG", "REACH", "ISO"],
  "eudr_readiness": "partial"
}
```

If you do not know exact Butler capability values, get them from the founder before writing code. Do not invent them.

---

### `bronze.raw_freight_benchmarks`

Store manually researched freight benchmarks.

```json
{
  "route": "Chennai to Hamburg",
  "mode": "sea",
  "container_type": "20ft",
  "currency": "USD",
  "benchmark_low": 1800,
  "benchmark_high": 2600,
  "as_of_date": "2026-01-15",
  "source": "Manual benchmark from public freight index"
}
```

Do not build live freight API integration for MVP. Use manually updated benchmarks with source and date.

---

## Silver Layer: Canonical Business Entities

Silver is where raw research becomes usable business data.

### Silver tables

```text
silver.buyers
silver.buyer_requirements
silver.compliance_records
silver.capabilities
silver.signals_normalized
silver.freight_benchmarks
```

---

## `silver.buyers`

Canonical buyer profile.

```text
id
name
country
website
segment
product_categories JSONB
procurement_model
import_dependency
target_materials JSONB
target_certifications JSONB
eudr_pressure_score
buyer_signal_score
source_confidence
last_reviewed_at
is_active
```

Example:

```json
{
  "name": "Picard",
  "country": "Germany",
  "segment": "Leather goods",
  "product_categories": ["bags", "accessories"],
  "procurement_model": "outsourced manufacturing / direct material sourcing",
  "import_dependency": "high",
  "target_materials": ["finished leather", "premium leather"],
  "target_certifications": ["LWG", "REACH", "EUDR due diligence"],
  "eudr_pressure_score": 80,
  "buyer_signal_score": 70,
  "source_confidence": "medium"
}
```

---

## `silver.buyer_requirements`

This is critical for matching.

```text
id
buyer_id
material_type
tannage
thickness_min_mm
thickness_max_mm
finish
color_requirements
certification_required
moq_tolerance
incoterms
notes
```

Example:

```json
{
  "buyer_id": "buyer_123",
  "material_type": "finished leather",
  "tannage": "chrome-free",
  "thickness_min_mm": 1.0,
  "thickness_max_mm": 1.4,
  "finish": "semi-aniline",
  "certification_required": "LWG",
  "moq_tolerance": "medium",
  "incoterms": "CIF",
  "notes": "Likely values traceability and consistent batch quality."
}
```

---

## `silver.compliance_records`

Use this for both Butler and buyers.

```text
id
entity_type
entity_id
standard
status
evidence_url
gap
severity
notes
updated_at
```

Examples:

```text
entity_type = butler
standard = EUDR traceability
status = partial
gap = Missing geolocation evidence for hide origin
severity = high
```

```text
entity_type = buyer
standard = EUDR due diligence
status = expected
gap = Buyer likely requires supplier due diligence package
severity = medium
```

---

## `silver.capabilities`

Butler’s canonical capability profile.

```text
id
company_name
location
material_type
tannage
thickness_min_mm
thickness_max_mm
finish
monthly_capacity_sqft
moq_sqft
lead_time_days
port_of_export
incoterms JSONB
certifications JSONB
eudr_readiness_score
notes
updated_at
```

For MVP, Butler can have one primary capability profile and optionally multiple material lines.

---

## `silver.signals_normalized`

Cleaned signals used in the Live Signals Feed.

```text
id
buyer_id nullable
category
title
body
source_url
signal_date
urgency
sentiment
impact
confidence
created_at
```

Categories:

```text
eudr
freight
buyer_activity
procurement
regulatory
market
```

---

## `silver.freight_benchmarks`

```text
id
route
mode
unit
currency
benchmark_low
benchmark_high
trend
as_of_date
source
```

Example routes:

```text
Chennai to Hamburg
Chennai to Antwerp
Chennai to Rotterdam
Chennai to Frankfurt air sample
```

---

# Gold Layer: Match Scores, Signals, and Actions

Gold is the business-value layer.

### Gold tables/views

```text
gold.match_scores
gold.match_drivers
gold.account_360
gold.actions
gold.v_match_portal
```

For MVP, Gold can be a mix of tables and SQL views. Do not overbuild.

---

## Match Score Formula

Use deterministic, explainable scoring. Do not make the MVP depend on embeddings or black-box AI.

Recommended MVP score:

```text
Total Match Score = 100

Capability Fit:        40 points
Compliance / EUDR:     30 points
Demand Signals:        20 points
Logistics Feasibility: 10 points
```

### Capability Fit — 40 points

```text
Material match:              15
Tannage / finish match:      10
MOQ / capacity fit:           8
Lead time fit:                7
```

### Compliance / EUDR — 30 points

```text
Certification overlap:       15
EUDR readiness alignment:    15
```

If Butler has missing EUDR evidence, reduce score but surface the gap as an action.

Example:

```text
Buyer requires EUDR traceability.
Butler has partial traceability.
Score reduced, but outreach recommends closing the gap.
```

That is useful. It creates a next action.

---

### Demand Signals — 20 points

Score recent buyer or market signals.

Examples:

```text
Buyer sustainability report mentions traceability
Buyer hiring sourcing/supply chain roles
Buyer expanding leather product line
Buyer attends leather trade fair
Public interest in non-EU sourcing
Regulatory pressure increases need for compliant suppliers
```

Use recency decay:

```text
0–30 days:   full score
31–90 days:  75%
91–180 days: 50%
older:       25%
```

---

### Logistics Feasibility — 10 points

```text
Chennai export route viable:       4
Incoterm alignment:                3
Freight benchmark acceptable:      3
```

For MVP, this can be rule-based.

---

## `gold.match_scores`

```text
id
buyer_id
capability_id
total_score
capability_score
compliance_score
signal_score
logistics_score
drivers JSONB
disqualifiers JSONB
computed_at
```

Example:

```json
{
  "buyer_id": "buyer_picard",
  "total_score": 82,
  "capability_score": 33,
  "compliance_score": 24,
  "signal_score": 17,
  "logistics_score": 8,
  "drivers": [
    "German leather goods buyer with likely import dependency",
    "Public sustainability/traceability language increases EUDR urgency",
    "Butler's finish and thickness range aligns with premium leather goods",
    "Chennai to Hamburg route is commercially viable"
  ],
  "disqualifiers": []
}
```

---

## `gold.account_360`

This powers Screen 3.

```text
buyer_id
summary
match_score
top_match_drivers JSONB
key_gaps JSONB
eudr_gap_summary
freight_summary
recommended_next_action
outreach_angle
updated_at
```

Example:

```json
{
  "summary": "German leather goods buyer with premium positioning and likely need for traceable finished leather.",
  "match_score": 82,
  "top_match_drivers": [
    "Material alignment",
    "EUDR pressure",
    "Chennai export feasibility"
  ],
  "key_gaps": [
    "Butler needs stronger EUDR geolocation evidence",
    "Need to confirm buyer's minimum order requirements"
  ],
  "recommended_next_action": "Send EUDR-aware capability introduction with sample offer.",
  "outreach_angle": "Position Butler's Leather as a Chennai-based EUDR-ready leather partner with premium finish capability."
}
```

---

## `gold.actions`

Store outreach generation and CRM push attempts.

```text
id
buyer_id
action_type
status
payload JSONB
created_at
```

Example:

```json
{
  "action_type": "outreach_generation",
  "status": "generated",
  "payload": {
    "subject": "EUDR-ready leather supply from Chennai",
    "body": "Dear sourcing team..."
  }
}
```

For MVP, CRM push can be a stub. Do not build native HubSpot/Zoho/Salesforce integration unless it takes less than one hour via webhook.

---

# 3. React Frontend MVP: The 3 Core Screens

Use a simple Vite + React + Tailwind + shadcn/ui structure.

Do not use Redux. Use TanStack Query.

---

## Recommended frontend file structure

```text
web/
  src/
    main.tsx
    App.tsx
    routes/
      RootLayout.tsx
      MatchPortalPage.tsx
      SignalsFeedPage.tsx
      Account360Page.tsx
    components/
      layout/
        AppShell.tsx
        TopNav.tsx
        PageHeader.tsx
      ui/
        button.tsx
        card.tsx
        badge.tsx
        table.tsx
        tabs.tsx
        dialog.tsx
        textarea.tsx
        toast.tsx
        skeleton.tsx
      match/
        CapabilityCard.tsx
        BuyerMatchCard.tsx
        MatchScoreBadge.tsx
        MatchReasonList.tsx
        MatchPortalEmptyState.tsx
      signals/
        SignalCard.tsx
        SignalCategoryTabs.tsx
        EUDRScorecard.tsx
        FreightBenchmarkCard.tsx
      account/
        AccountHeader.tsx
        AccountSummaryCard.tsx
        MatchDriversCard.tsx
        ComplianceGapTable.tsx
        SignalTimeline.tsx
        ActionPanel.tsx
        OutreachDrawer.tsx
        CRMStubButton.tsx
    lib/
      api.ts
      queryClient.ts
      types.ts
      formatters.ts
```

---

# Screen 1: Match Portal

Route:

```text
/
```

Purpose:

> Show Butler’s capability card and the top 5 ranked European buyers.

This screen must answer:

1. What can Butler’s Leather supply?
2. Which European buyers are most worth contacting?
3. Why are they ranked?
4. What is the next action?

---

## Component structure

```text
MatchPortalPage
  PageHeader
  CapabilityCard
  BuyerMatchList
    BuyerMatchCard
      MatchScoreBadge
      BuyerSummary
      MatchReasonList
      ViewAccountButton
```

---

## `CapabilityCard`

Display:

```text
Company: Butler's Leather
Location: Chennai, India
Export focus: EU / Germany
Material types
Tannage
Thickness range
Finish
MOQ
Monthly capacity
Lead time
Port
Incoterms
Certifications
EUDR readiness
```

Use shadcn:

```text
Card
Badge
Separator
Button
```

---

## `BuyerMatchCard`

Display:

```text
Rank
Buyer name
Country
Segment
Match score
Top 3 match reasons
Key gap
CTA: View Account 360
```

Example UI copy:

```text
#1 Picard
Germany — Leather Goods
Match Score: 82

Why matched:
- Likely demand for premium finished leather
- Public sustainability/traceability language
- Chennai to Hamburg logistics viable

Gap:
- Confirm exact material specifications and MOQ

[View Account 360]
```

---

## API endpoints for Screen 1

### `GET /api/v1/capability`

Returns Butler’s capability profile.

Response:

```json
{
  "company_name": "Butler's Leather",
  "location": "Chennai, India",
  "material_types": ["finished leather"],
  "tannage": ["vegetable", "chrome", "chrome-free"],
  "thickness_range_mm": ["0.8", "1.4"],
  "finish": ["aniline", "semi-aniline", "pigmented"],
  "moq_sqft": 3000,
  "monthly_capacity_sqft": 50000,
  "lead_time_days": 30,
  "port_of_export": "Chennai",
  "incoterms": ["FOB", "CIF", "EXW"],
  "certifications": ["LWG", "REACH"],
  "eudr_readiness_score": 58
}
```

---

### `GET /api/v1/matches?limit=5`

Returns top ranked buyers.

Response:

```json
{
  "generated_at": "2026-01-20T09:00:00Z",
  "capability_id": "butler_chennai_v1",
  "matches": [
    {
      "buyer_id": "buyer_picard",
      "rank": 1,
      "name": "Picard",
      "country": "Germany",
      "segment": "Leather goods",
      "total_score": 82,
      "capability_score": 33,
      "compliance_score": 24,
      "signal_score": 17,
      "logistics_score": 8,
      "top_reasons": [
        "Likely demand for premium finished leather",
        "Public sustainability/traceability language",
        "Chennai to Hamburg logistics viable"
      ],
      "key_gap": "Confirm exact material specifications and MOQ",
      "recommended_action": "Send EUDR-aware capability introduction"
    }
  ]
}
```

---

# Screen 2: Live Signals Feed

Route:

```text
/signals
```

Purpose:

> Show market, EUDR, freight, and buyer signals that justify action.

This screen must answer:

1. Why should Butler act now?
2. Where are the EUDR gaps?
3. What is the freight context?
4. Which signals are buyer-specific?

---

## Component structure

```text
SignalsFeedPage
  PageHeader
  EUDRScorecard
  FreightBenchmarkCard
  SignalCategoryTabs
  SignalList
    SignalCard
```

---

## `EUDRScorecard`

This is one of the highest-value MVP components.

Display:

```text
Butler's EUDR Readiness Score
Required evidence
Completed
Partial
Missing
Top gap
Recommended fix
```

Example:

```text
EUDR Readiness: 58/100

Completed:
- Supplier declarations partially collected
- Tannery compliance records available

Partial:
- Hide origin traceability
- Deforestation cut-off evidence

Missing:
- Geolocation polygons
- Formal due diligence statement workflow

Recommended next step:
Create EUDR evidence pack before outreach to high-pressure EU buyers.
```

Do not present this as legal advice. Label it:

```text
Decision-support view. Verify current EUDR requirements before external claims.
```

---

## `FreightBenchmarkCard`

Display:

```text
Route
Mode
Benchmark range
Trend
As-of date
Source
Commercial implication
```

Example:

```text
Chennai to Hamburg
Sea freight — 20ft
Benchmark: $1,800–$2,600
Trend: Stable
As of: Jan 15, 2026
Source: Manual public benchmark

Implication:
FOB Chennai pricing remains competitive for EU buyers if lead times are managed.
```

---

## `SignalCard`

Display:

```text
Signal category
Date
Title
Impact
Confidence
Source link
Related buyer, if any
```

Example:

```text
EUDR — High urgency
European buyers increasing supplier traceability expectations.
Impact: Suppliers with EUDR evidence packs gain early access.
Source: Public sustainability report
Confidence: Medium
```

---

## API endpoints for Screen 2

### `GET /api/v1/signals?limit=20&category=eudr`

Response:

```json
{
  "signals": [
    {
      "id": "signal_001",
      "category": "eudr",
      "title": "EU buyers increasing traceability expectations",
      "body": "Public buyer communications indicate stronger focus on deforestation-free supply chains.",
      "signal_date": "2026-01-10",
      "urgency": "high",
      "confidence": "medium",
      "source_url": "https://example.com",
      "buyer_id": null
    }
  ]
}
```

---

### `GET /api/v1/eudr-scorecard`

Response:

```json
{
  "entity": "Butler's Leather",
  "readiness_score": 58,
  "status": "partial",
  "requirements": [
    {
      "requirement": "Hide origin traceability",
      "status": "partial",
      "severity": "high"
    },
    {
      "requirement": "Geolocation evidence",
      "status": "missing",
      "severity": "high"
    },
    {
      "requirement": "Supplier due diligence declarations",
      "status": "partial",
      "severity": "medium"
    },
    {
      "requirement": "Deforestation cut-off evidence",
      "status": "missing",
      "severity": "high"
    }
  ],
  "top_gap": "Missing geolocation and formal due diligence evidence.",
  "recommended_action": "Assemble EUDR evidence pack before contacting high-pressure buyers."
}
```

---

### `GET /api/v1/freight-benchmarks`

Response:

```json
{
  "benchmarks": [
    {
      "route": "Chennai to Hamburg",
      "mode": "sea",
      "unit": "20ft container",
      "currency": "USD",
      "benchmark_low": 1800,
      "benchmark_high": 2600,
      "trend": "stable",
      "as_of_date": "2026-01-15",
      "source": "Manual public benchmark"
    }
  ]
}
```

---

# Screen 3: Account 360 & 1-Click Action

Route:

```text
/accounts/:buyerId
```

Purpose:

> Give Butler a complete buyer view and generate the next outreach action immediately.

This screen must answer:

1. Who is this buyer?
2. Why did Trade OS rank them?
3. What are the gaps?
4. What should Butler say?
5. How do we push this to CRM or email?

---

## Component structure

```text
Account360Page
  AccountHeader
  AccountSummaryCard
  MatchDriversCard
  ComplianceGapTable
  SignalTimeline
  ActionPanel
    OutreachDrawer
    CRMStubButton
```

---

## `AccountHeader`

Display:

```text
Buyer name
Country
Segment
Website
Match score
Last updated
Source confidence
```

---

## `AccountSummaryCard`

Display:

```text
Buyer summary
Procurement model
Likely material needs
Likely certifications
Recommended next action
```

---

## `MatchDriversCard`

Display top reasons:

```text
- Material alignment
- EUDR pressure
- Logistics feasibility
- Recent buyer signal
```

---

## `ComplianceGapTable`

Display:

```text
Requirement
Buyer expectation
Butler status
Gap
Severity
Action
```

Example:

```text
EUDR traceability | Required | Partial | Need geolocation evidence | High
LWG certification | Preferred | Available | None | Low
REACH compliance | Required | Available | None | Low
```

---

## `SignalTimeline`

Display buyer-specific and market signals.

```text
Jan 12 — Buyer sustainability report mentions traceability
Jan 10 — EUDR pressure increasing in EU leather goods segment
Jan 05 — Freight benchmark stable on Chennai-Hamburg route
```

---

## `ActionPanel`

This is the money component.

Buttons:

```text
Generate Outreach
Copy Email
Download CRM JSON
Mark as Contacted
```

For MVP, “CRM push” can mean:

```text
Generate structured JSON
Copy to clipboard
Download CSV/JSON
Send to webhook if already available
```

Do not build a full CRM connector.

---

## `OutreachDrawer`

Use a shadcn Sheet/Dialog.

Fields:

```text
To
Subject
Body
Tone
CTA
Copy button
Edit button
```

For MVP, use deterministic templates first. LLM optional.

---

## API endpoints for Screen 3

### `GET /api/v1/accounts/{buyer_id}`

Response:

```json
{
  "buyer_id": "buyer_picard",
  "name": "Picard",
  "country": "Germany",
  "segment": "Leather goods",
  "website": "https://www.picard.de",
  "match_score": 82,
  "summary": "German leather goods buyer with premium positioning and likely need for traceable finished leather.",
  "top_match_drivers": [
    "Material alignment",
    "EUDR pressure",
    "Chennai export feasibility"
  ],
  "key_gaps": [
    "Butler needs stronger EUDR geolocation evidence",
    "Need to confirm buyer's minimum order requirements"
  ],
  "recommended_next_action": "Send EUDR-aware capability introduction with sample offer.",
  "source_confidence": "medium",
  "last_updated": "2026-01-20T09:00:00Z"
}
```

---

### `GET /api/v1/accounts/{buyer_id}/signals`

Response:

```json
{
  "signals": [
    {
      "id": "signal_101",
      "category": "buyer_activity",
      "title": "Buyer emphasizes responsible sourcing",
      "signal_date": "2026-01-12",
      "urgency": "medium",
      "source_url": "https://example.com"
    }
  ]
}
```

---

### `POST /api/v1/accounts/{buyer_id}/outreach`

Request:

```json
{
  "tone": "professional",
  "include_eudr": true,
  "include_sample_offer": true,
  "sender_name": "Butler's Leather Export Team"
}
```

Response:

```json
{
  "action_id": "action_500",
  "buyer_id": "buyer_picard",
  "subject": "Traceable leather supply from Chennai for EU sourcing",
  "body": "Dear sourcing team,\n\nButler's Leather is a Chennai-based leather exporter supporting premium leather goods manufacturers with traceable material supply...\n\nWe would welcome the opportunity to share specifications, compliance documentation, and sample options.\n\nBest regards,\nButler's Leather Export Team",
  "status": "generated"
}
```

---

### `POST /api/v1/accounts/{buyer_id}/crm-push`

For MVP, this can return a queued stub.

Request:

```json
{
  "action_id": "action_500",
  "destination": "manual_csv"
}
```

Response:

```json
{
  "status": "queued_stub",
  "message": "CRM push is stubbed for MVP. Use download or copy.",
  "download_format": "json"
}
```

If Butler uses Zoho, HubSpot, or Pipedrive, do not build native integration unless you can do a simple webhook in under one hour.

---

# 4. Critical Traps to Avoid

## Do NOT build these in the MVP

### 1. Do not build real-time scraping

Manual CSV/JSON seeding is enough.

Scraping creates:

- legal risk
- brittle data
- engineering delay
- false confidence

For MVP, use manual research with source links.

---

### 2. Do not build a full EUDR compliance engine

EUDR is complex and legally sensitive.

Your MVP should provide:

```text
gap visibility
evidence checklist
outreach framing
```

It should not say:

```text
Butler is EUDR compliant
```

unless verified by proper legal/compliance review.

Use language like:

```text
EUDR readiness indicator
Decision-support view
Evidence gap summary
```

---

### 3. Do not build vector search as the core matching method

pgvector can be installed, but do not make the MVP depend on it.

Use deterministic scoring first.

Why?

Because Butler needs to trust the match explanation.

A buyer match must say:

```text
Matched because:
- Material alignment
- Certification overlap
- Recent buyer signal
- Logistics feasibility
```

Not:

```text
Matched because embedding similarity was 0.82
```

---

### 4. Do not build multi-tenant SaaS yet

This MVP is for one customer: Butler’s Leather.

Do not build:

- organizations
- roles
- permissions
- invite flows
- billing
- subscription management

Use a simple demo login or passcode if needed.

---

### 5. Do not build a CRM integration

For MVP, CRM push means:

```text
structured action record
copyable email
downloadable JSON/CSV
optional webhook stub
```

That is enough.

---

### 6. Do not build live freight APIs

Use manually updated freight benchmarks.

Show:

```text
route
mode
range
as-of date
source
```

That is commercially useful.

---

### 7. Do not build notifications

No email alerts.

No Slack alerts.

No push notifications.

The UI should be pull-based for MVP.

---

### 8. Do not build admin CRUD

Seed data through scripts.

If the founder wants to edit data, update the seed file and redeploy.

Do not waste days on admin screens.

---

# 5. Fastest Path From Code to Closing the $500 Pilot

Your goal is not to sell software.

Your goal is to sell a outcome:

> More qualified European buyer conversations for Butler’s Leather.

---

## Pilot Offer

Package the MVP as a paid pilot:

```text
Trade OS Export Pilot — Butler's Leather
Price: $500
Duration: 14 days
```

Deliverables:

```text
1. 10 ranked European buyer matches
2. Buyer match scorecards with reasons
3. EUDR gap scorecard
4. Freight benchmark view
5. 10 personalized outreach emails
6. CRM-ready export
7. 2-week support and iteration
```

Success target:

```text
2 qualified buyer conversations
or
1 sample request / RFQ
```

Do not promise orders. Promise pipeline creation.

---

## Pilot One-Pager Copy

Use something like:

```text
Trade OS Export Pilot for Butler's Leather

Trade OS identifies high-fit European leather buyers, scores them against Butler's Chennai export capabilities, and generates EUDR-aware outreach.

Pilot deliverables:
- 10 ranked EU buyer matches
- Match reasons and gap analysis
- EUDR readiness scorecard
- Freight benchmark snapshot
- 10 personalized outreach emails
- CRM-ready export

Pilot outcome:
Start qualified conversations with European buyers faster.

Price: $500
Duration: 14 days
```

---

## Sales Script for the Founder Call

Use this:

```text
The goal of this pilot is not to give you another dashboard.

The goal is to identify the five to ten European buyers most likely to respond to Butler's Leather, explain why they are worth contacting, and generate outreach that addresses their likely material, compliance, and EUDR concerns.

For the pilot, we will deliver a ranked buyer list, an EUDR gap scorecard, freight benchmarks, and ready-to-send outreach.

If this creates two qualified conversations, the pilot pays for itself.
```

---

## Close the Pilot in 5 Steps

### Step 1: Show the Match Portal

Open Screen 1.

Say:

```text
These are the five buyers Trade OS currently ranks highest for Butler's Leather.
```

Click into one buyer.

Show:

```text
match score
match reasons
gap
recommended action
```

---

### Step 2: Show the EUDR Gap

Open Screen 2.

Say:

```text
European buyers are increasingly sensitive to traceability and EUDR evidence. This scorecard shows where Butler is strong and where the evidence gap needs to be closed.
```

This makes the product feel strategic, not just cosmetic.

---

### Step 3: Show Account 360

Open Screen 3.

Say:

```text
This is the full buyer view. Trade OS tells us why this buyer matters, what gaps exist, and what to say next.
```

---

### Step 4: Generate Outreach Live

Click:

```text
Generate Outreach
```

Then say:

```text
This gives your team a ready-to-send email that connects Butler's capability to the buyer's likely need.
```

This is the moment the product becomes practical.

---

### Step 5: Ask for the Pilot

Say:

```text
We can run this as a 14-day paid pilot for $500. You get the ranked buyer list, EUDR gap view, freight benchmarks, and outreach pack. Our target is to create two qualified buyer conversations.
```

Then stop talking.

Let them respond.

---

# 6. 7–10 Day Execution Plan

## Day 1: Lock MVP Scope and Data

Deliverables:

```text
Final capability profile for Butler's Leather
20–30 European buyer candidates
10–20 signals
Freight benchmark entries
Match score formula approved
```

Do not start coding until the capability profile is real.

Required Butler fields:

```text
material types
tannage
thickness range
finish
MOQ
capacity
lead time
certifications
export port
incoterms
EUDR readiness
```

---

## Day 2: Bronze + Silver Schema

Build:

```text
Postgres schemas
Bronze tables
Silver tables
Seed scripts
```

Commands:

```bash
make seed-bronze
make transform-silver
```

Definition of done:

```text
Raw buyer data loads into bronze
Clean buyer data appears in silver
Capability profile appears in silver
Signals appear in silver
Freight benchmarks appear in silver
```

---

## Day 3: Gold Scoring

Build:

```text
gold.match_scores
gold.account_360
scoring script
match drivers
```

Definition of done:

```text
Top 5 buyers can be ranked
Each buyer has match reasons
Each buyer has gaps
Score is explainable
```

---

## Day 4: FastAPI Endpoints

Build:

```text
GET /health
GET /api/v1/capability
GET /api/v1/matches
GET /api/v1/signals
GET /api/v1/eudr-scorecard
GET /api/v1/freight-benchmarks
GET /api/v1/accounts/{id}
GET /api/v1/accounts/{id}/signals
POST /api/v1/accounts/{id}/outreach
POST /api/v1/accounts/{id}/crm-push
```

Definition of done:

```text
OpenAPI docs work
All endpoints return seeded data
No endpoint depends on unstable external APIs
```

---

## Day 5: Screen 1 — Match Portal

Build:

```text
CapabilityCard
BuyerMatchCard
MatchScoreBadge
MatchReasonList
```

Definition of done:

```text
Butler capability visible
Top 5 buyers visible
Match reasons visible
Account link works
```

---

## Day 6: Screen 2 — Signals Feed

Build:

```text
SignalCard
EUDRScorecard
FreightBenchmarkCard
SignalCategoryTabs
```

Definition of done:

```text
Signals load
EUDR scorecard visible
Freight benchmark visible
Source links visible
```

---

## Day 7: Screen 3 — Account 360 + Outreach

Build:

```text
AccountHeader
AccountSummaryCard
MatchDriversCard
ComplianceGapTable
SignalTimeline
ActionPanel
OutreachDrawer
```

Definition of done:

```text
Account 360 loads
Outreach generation works
Copy button works
CRM stub works
```

---

## Day 8: Polish and Deploy

Deploy stack:

```text
Frontend: Vercel or Netlify
Backend: Render, Railway, or Fly.io
Database: Neon, Supabase, or managed Postgres
```

Definition of done:

```text
Public demo URL works
API URL works
No console errors
Loading states exist
Empty states exist
Toasts work
Demo is stable
```

If you need simple protection, use a passcode or basic auth. Do not build full auth.

---

## Day 9: Pilot Demo and Sales Assets

Create:

```text
Demo script
Pilot one-pager
Invoice/payment link
Sample outreach pack
Buyer evidence sheet
```

Definition of done:

```text
Founder can demo in 10 minutes
Pilot offer is clear
Payment method exists
```

---

## Day 10: Buffer and Close

Use this day for:

```text
data corrections
UI fixes
founder feedback
outreach tone tuning
closing the pilot
```

---

# 7. MVP Definition of Done

You are done when the following are true:

```text
1. Butler's capability card is accurate.
2. At least 20 European buyers are seeded.
3. At least 5 buyers are ranked with explainable scores.
4. At least 10 signals are visible.
5. EUDR scorecard is visible.
6. Freight benchmark is visible.
7. Account 360 works for each top buyer.
8. Outreach generation works.
9. CRM export stub works.
10. Demo URL is stable.
11. Pilot one-pager exists.
12. Founder can present it in under 10 minutes.
```

If you have all of these, you have a commercial MVP.

---

# 8. Technical Implementation Rules

## Use Postgres schemas, not separate data platforms

```sql
bronze.raw_buyers
silver.buyers
gold.match_scores
```

That is enough.

---

## Use JSONB where flexible, relational where valuable

Use JSONB for:

```text
raw payloads
match drivers
gap lists
outreach metadata
```

Use relational tables for:

```text
buyers
capabilities
signals
compliance records
freight benchmarks
match scores
actions
```

---

## Use pgvector only optionally

Install it:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

But do not make MVP matching depend on it.

If used later, it can support:

```text
buyer capability text similarity
signal semantic search
outreach personalization
```

Not now.

---

## Use deterministic scoring

The founder must be able to understand why a buyer is ranked.

Every match must have:

```text
score
reasons
gaps
recommended action
```

---

## Use source links everywhere

Every buyer, signal, and benchmark should have:

```text
source_url
source_confidence
as_of_date
```

This builds trust.

---

## Use manual overrides

Add fields like:

```text
manual_override
review_status
reviewed_by
reviewed_at
```

For MVP, human review is a feature, not a weakness.

---

# 9. What Makes This MVP High-Impact

The MVP is high-impact if it does three things extremely well:

## 1. It ranks buyers

Not lists. Ranks.

With reasons.

---

## 2. It exposes gaps

Especially:

```text
EUDR gaps
material specification gaps
certification gaps
logistics gaps
```

Gaps create consulting value and next actions.

---

## 3. It creates outreach

The product must end in action.

If the user finishes the flow with a ready-to-send email, the product feels useful immediately.

---

# 10. Final Advice

Do not try to make this perfect.

Make it:

```text
specific
explainable
commercially useful
fast
stable
```

Your MVP should feel like this:

```text
Butler's Leather capability
        ↓
Top 5 European buyers
        ↓
Why they match
        ↓
What gaps exist
        ↓
What market signals support action
        ↓
One-click outreach
```

That is the product.

Everything else is Phase 2.

The fastest path to the $500 pilot is not more engineering. It is a sharp demo with real buyer names, real Butler capabilities, real EUDR gaps, and a ready-to-send outreach pack.

Ship the smallest version that creates a buyer conversation. Then expand.