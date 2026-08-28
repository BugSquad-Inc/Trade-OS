

# TRADE OS — MASTER PROTOTYPE EXECUTION, IMMEDIATE VALIDATION & FUTURE SCALING PLAN  
## Butler’s Leather, Chennai — Finished Cow/Goat Leather Export to Germany/Europe  
### Permanent Build-and-Scale Manual: Prototype → Paid Pilot → Subscription → Enterprise Platform

---

# 0. EXECUTIVE SUMMARY

Trade OS is being built as a vertical B2B intelligence and revenue-generation system for Butler’s Leather, Chennai.

The immediate commercial objective is simple:

> **Sell a $500 paid pilot with a 14-day, 5-qualified-match guarantee.**  
> Convert the pilot into a **$950/month subscription**.  
> Expand into adjacent leather ecosystem categories and later package a **$2,500/month Enterprise Tier**.

The prototype must not look like a dashboard. It must feel like a **deal-flow engine**:

1. It shows qualified buyers.
2. It explains why each buyer matters.
3. It shows live buying signals.
4. It gives a one-click next action.
5. It produces outreach-ready messaging.
6. It creates a defensible path from raw data to revenue.

The first customer is Butler’s Leather, exporting finished cow/goat leather to Germany/Europe.

The first five demo buyer dossiers should include:

1. **Picard**
2. **Roeckl**
3. **Bader**
4. **Kilger**
5. **Otto Schumacher**

These must be presented not as generic leads, but as **qualified match dossiers** with evidence, fit rationale, intent signals, risk notes, and recommended outreach.

---

# SECTION 1  
# END-TO-END PROTOTYPE ARCHITECTURE & CODEBASE BLUEPRINT

---

## 1.1 PRODUCT ARCHITECTURE PRINCIPLES

Trade OS MVP must follow five rules:

1. **Single-tenant first, multi-tenant later**  
   The MVP is scoped for Butler’s Leather, but the schema must not paint us into a corner. Add organization/tenant fields in Phase 2.

2. **Medallion data architecture**  
   Use three PostgreSQL schemas:

   - `bronze`: raw, immutable ingestion layer.
   - `silver`: cleaned, normalized, entity-resolved business entities.
   - `gold`: commercial outputs — matches, account 360, outreach tasks, KPIs.

3. **Revenue-first data model**  
   Every table should ultimately support one of these questions:

   - Who should Butler’s Leather contact?
   - Why now?
   - What product fits?
   - Who is the right person?
   - What message should be sent?
   - What happened after outreach?

4. **Demo must be deterministic**  
   The prototype should not depend on live scraping during the sales demo. Use seeded, verified, curated data for the first five buyer dossiers.

5. **Manual intelligence first, automation second**  
   For the paid pilot, human-verified matches are better than noisy automated matches. Automation is introduced after the commercial motion is proven.

---

## 1.2 EXACT REPOSITORY STRUCTURE

Create a clean workspace named:

```bash
Trade OS/
```

Use this exact structure:

```bash
Trade OS/
├── README.md
├── Makefile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── docs/
│   ├── architecture.md
│   ├── api_contract.md
│   ├── data_dictionary.md
│   ├── demo_script.md
│   ├── pilot_agreement.md
│   ├── buyer_dossier_verification.md
│   └── scaling_roadmap.md
│
├── backend/
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── pyproject.toml
│   ├── .env.example
│   │
│   ├── alembic/
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 0001_initial_trade_os_schema.py
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── init_db.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── bronze.py
│   │   │   ├── silver.py
│   │   │   └── gold.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── common.py
│   │   │   ├── account.py
│   │   │   ├── contact.py
│   │   │   ├── product.py
│   │   │   ├── signal.py
│   │   │   ├── match.py
│   │   │   └── outreach.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── health.py
│   │   │           ├── matches.py
│   │   │           ├── signals.py
│   │   │           ├── accounts.py
│   │   │           └── outreach.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── account_service.py
│   │   │   ├── match_service.py
│   │   │   ├── signal_service.py
│   │   │   ├── outreach_service.py
│   │   │   └── scoring_service.py
│   │   │
│   │   ├── data/
│   │   │   └── seed/
│   │   │       ├── demo_seed.json
│   │   │       ├── hs_codes.json
│   │   │       ├── buyer_dossiers.json
│   │   │       └── outreach_templates.json
│   │   │
│   │   └── scripts/
│   │       ├── __init__.py
│   │       ├── seed_db.py
│   │       ├── verify_demo_data.py
│   │       └── generate_match_scores.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_health.py
│       ├── test_matches.py
│       ├── test_signals.py
│       ├── test_accounts.py
│       └── test_outreach.py
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── index.html
│   ├── .env.example
│   │
│   ├── public/
│   │   └── favicon.svg
│   │
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── routes.tsx
│       │
│       ├── api/
│       │   ├── client.ts
│       │   ├── health.ts
│       │   ├── matches.ts
│       │   ├── signals.ts
│       │   ├── accounts.ts
│       │   └── outreach.ts
│       │
│       ├── types/
│       │   ├── account.ts
│       │   ├── contact.ts
│       │   ├── product.ts
│       │   ├── signal.ts
│       │   ├── match.ts
│       │   └── outreach.ts
│       │
│       ├── lib/
│       │   ├── utils.ts
│       │   ├── constants.ts
│       │   └── formatters.ts
│       │
│       ├── hooks/
│       │   ├── useHealth.ts
│       │   ├── useMatches.ts
│       │   ├── useSignals.ts
│       │   ├── useAccount.ts
│       │   └── useOutreach.ts
│       │
│       ├── components/
│       │   ├── ui/
│       │   │   ├── button.tsx
│       │   │   ├── card.tsx
│       │   │   ├── badge.tsx
│       │   │   ├── input.tsx
│       │   │   ├── select.tsx
│       │   │   ├── dialog.tsx
│       │   │   ├── drawer.tsx
│       │   │   ├── table.tsx
│       │   │   ├── tabs.tsx
│       │   │   ├── skeleton.tsx
│       │   │   ├── toast.tsx
│       │   │   └── tooltip.tsx
│       │   │
│       │   ├── layout/
│       │   │   ├── AppShell.tsx
│       │   │   ├── Sidebar.tsx
│       │   │   ├── Topbar.tsx
│       │   │   ├── PageHeader.tsx
│       │   │   └── EmptyState.tsx
│       │   │
│       │   └── shared/
│       │       ├── ScoreBadge.tsx
│       │       ├── SignalBadge.tsx
│       │       ├── CountryFlag.tsx
│       │       ├── EvidenceLink.tsx
│       │       ├── LoadingPanel.tsx
│       │       ├── ErrorPanel.tsx
│       │       └── CopyButton.tsx
│       │
│       ├── features/
│       │   ├── matches/
│       │   │   ├── MatchPortalPage.tsx
│       │   │   ├── MatchFilterBar.tsx
│       │   │   ├── MatchTable.tsx
│       │   │   ├── MatchCard.tsx
│       │   │   ├── MatchScorePanel.tsx
│       │   │   ├── MatchDrawer.tsx
│       │   │   ├── MatchRationale.tsx
│       │   │   ├── MatchEvidenceList.tsx
│       │   │   └── MatchActionBar.tsx
│       │   │
│       │   ├── signals/
│       │   │   ├── LiveSignalsFeedPage.tsx
│       │   │   ├── SignalFilterBar.tsx
│       │   │   ├── SignalStream.tsx
│       │   │   ├── SignalCard.tsx
│       │   │   ├── SignalDetailDrawer.tsx
│       │   │   ├── SignalEntityTags.tsx
│       │   │   └── SignalSourceBadge.tsx
│       │   │
│       │   ├── accounts/
│       │   │   ├── Account360Page.tsx
│       │   │   ├── AccountHeader.tsx
│       │   │   ├── AccountTabs.tsx
│       │   │   ├── AccountOverviewPanel.tsx
│       │   │   ├── AccountSignalsPanel.tsx
│       │   │   ├── AccountContactsPanel.tsx
│       │   │   ├── AccountProductsPanel.tsx
│       │   │   ├── AccountOutreachPanel.tsx
│       │   │   ├── OneClickActionPanel.tsx
│       │   │   └── OutreachComposerDialog.tsx
│       │   │
│       │   └── outreach/
│       │       ├── OutreachTaskTable.tsx
│       │       ├── OutreachTemplateSelector.tsx
│       │       └── OutreachPreview.tsx
│       │
│       └── styles/
│           └── globals.css
│
└── scripts/
    ├── bootstrap.sh
    ├── seed_demo.sh
    ├── run_api.sh
    ├── run_web.sh
    └── verify_demo.sh
```

---

## 1.3 LOCAL RUNTIME ARCHITECTURE

For the prototype, run three local services:

```bash
PostgreSQL 16
FastAPI backend
React frontend
```

Architecture flow:

```text
React Frontend
    |
    | HTTP JSON
    v
FastAPI Backend
    |
    | SQLAlchemy / SQL
    v
PostgreSQL
    |
    ├── bronze: raw ingestion
    ├── silver: normalized entities
    └── gold: matches, account 360, outreach, KPIs
```

For demo reliability:

- Do not depend on live scraping.
- Seed the database with verified demo data.
- Use deterministic scores.
- Cache frontend queries.
- Have a local fallback JSON export if needed.

---

## 1.4 EXACT POSTGRESQL DDL FOR TRADE OS MVP

Use PostgreSQL 16.

This DDL creates the three medallion schemas:

- `bronze`
- `silver`
- `gold`

It is scoped for Butler’s Leather but designed for future multi-category expansion.

```sql
-- ============================================================
-- TRADE OS MVP DDL
-- Target: Butler's Leather Chennai
-- Schemas: bronze, silver, gold
-- PostgreSQL 16
-- ============================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Future Phase 2/3:
-- CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- ============================================================
-- UPDATED_AT TRIGGER FUNCTION
-- ============================================================

CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- BRONZE SCHEMA
-- Raw immutable ingestion layer
-- ============================================================

CREATE TABLE IF NOT EXISTS bronze.raw_sources (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_key text NOT NULL UNIQUE,
    source_type text NOT NULL CHECK (
        source_type IN (
            'manual',
            'csv',
            'scrape',
            'rss',
            'api',
            'email',
            'customs',
            'trade_show',
            'linkedin',
            'news'
        )
    ),
    uri text,
    content_hash text NOT NULL UNIQUE,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    fetched_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS bronze.raw_accounts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid REFERENCES bronze.raw_sources(id) ON DELETE SET NULL,
    account_key text NOT NULL,
    raw_name text NOT NULL,
    raw_domain text,
    raw_country text,
    raw_payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    ingested_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (source_id, account_key)
);

CREATE TABLE IF NOT EXISTS bronze.raw_signals (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid REFERENCES bronze.raw_sources(id) ON DELETE SET NULL,
    raw_account_key text,
    signal_type text NOT NULL CHECK (
        signal_type IN (
            'buying_intent',
            'product_launch',
            'hiring',
            'expansion',
            'regulatory',
            'tender',
            'news',
            'social',
            'customs',
            'event'
        )
    ),
    raw_title text NOT NULL,
    raw_text text,
    raw_url text,
    published_at timestamptz,
    content_hash text UNIQUE,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    ingested_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS bronze.raw_outreach_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid REFERENCES bronze.raw_sources(id) ON DELETE SET NULL,
    raw_account_key text,
    raw_contact_key text,
    channel text NOT NULL CHECK (
        channel IN (
            'email',
            'linkedin',
            'phone',
            'whatsapp',
            'event',
            'manual'
        )
    ),
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    occurred_at timestamptz NOT NULL DEFAULT now()
);

-- ============================================================
-- SILVER SCHEMA
-- Cleaned and normalized business entities
-- ============================================================

CREATE TABLE IF NOT EXISTS silver.accounts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_key text NOT NULL UNIQUE,
    name text NOT NULL,
    domain text,
    country text,
    region text,
    industry text,
    sub_industry text,
    hq_city text,
    website text,
    linkedin_url text,
    import_hs_codes text[],
    product_categories text[],
    compliance_requirements text[],
    employee_range text,
    status text NOT NULL DEFAULT 'prospect' CHECK (
        status IN (
            'active',
            'inactive',
            'prospect',
            'customer',
            'blocked'
        )
    ),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS silver_accounts_country_idx
ON silver.accounts(country);

CREATE INDEX IF NOT EXISTS silver_accounts_status_idx
ON silver.accounts(status);

CREATE INDEX IF NOT EXISTS silver_accounts_name_trgm_idx
ON silver.accounts USING gin (name gin_trgm_ops);

CREATE TABLE IF NOT EXISTS silver.contacts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL REFERENCES silver.accounts(id) ON DELETE CASCADE,
    full_name text NOT NULL,
    title text,
    email text,
    phone text,
    linkedin_url text,
    is_primary boolean NOT NULL DEFAULT false,
    confidence numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        confidence >= 0 AND confidence <= 1
    ),
    source text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS silver_contacts_account_email_unique_idx
ON silver.contacts(account_id, lower(email))
WHERE email IS NOT NULL;

CREATE INDEX IF NOT EXISTS silver_contacts_account_idx
ON silver.contacts(account_id);

CREATE TABLE IF NOT EXISTS silver.products (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL REFERENCES silver.accounts(id) ON DELETE CASCADE,
    product_type text NOT NULL CHECK (
        product_type IN (
            'supplier_catalog',
            'buyer_requirement',
            'chemical',
            'machinery',
            'accessory',
            'finished_leather'
        )
    ),
    name text NOT NULL,
    material text,
    hs_code text,
    color text,
    thickness_min_mm numeric(8,2),
    thickness_max_mm numeric(8,2),
    size_range text,
    moq_sqft numeric(12,2),
    target_price numeric(14,2),
    currency text,
    certification text[],
    notes text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS silver_products_account_idx
ON silver.products(account_id);

CREATE INDEX IF NOT EXISTS silver_products_hs_code_idx
ON silver.products(hs_code);

CREATE TABLE IF NOT EXISTS silver.signals (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid REFERENCES silver.accounts(id) ON DELETE CASCADE,
    signal_type text NOT NULL CHECK (
        signal_type IN (
            'buying_intent',
            'product_launch',
            'hiring',
            'expansion',
            'regulatory',
            'tender',
            'news',
            'social',
            'customs',
            'event'
        )
    ),
    title text NOT NULL,
    url text,
    snippet text,
    published_at timestamptz,
    score numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        score >= 0 AND score <= 100
    ),
    entity jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS silver_signals_url_unique_idx
ON silver.signals(url)
WHERE url IS NOT NULL;

CREATE INDEX IF NOT EXISTS silver_signals_account_idx
ON silver.signals(account_id);

CREATE INDEX IF NOT EXISTS silver_signals_published_at_idx
ON silver.signals(published_at DESC);

CREATE INDEX IF NOT EXISTS silver_signals_type_idx
ON silver.signals(signal_type);

CREATE TABLE IF NOT EXISTS silver.capabilities (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid NOT NULL REFERENCES silver.accounts(id) ON DELETE CASCADE,
    capability_key text NOT NULL,
    capability_value text NOT NULL,
    confidence numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        confidence >= 0 AND confidence <= 1
    ),
    source text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (account_id, capability_key)
);

-- ============================================================
-- GOLD SCHEMA
-- Commercial output layer
-- ============================================================

CREATE TABLE IF NOT EXISTS gold.matches (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_account_id uuid NOT NULL REFERENCES silver.accounts(id) ON DELETE CASCADE,
    buyer_account_id uuid NOT NULL REFERENCES silver.accounts(id) ON DELETE CASCADE,
    product_id uuid REFERENCES silver.products(id) ON DELETE SET NULL,
    match_score numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        match_score >= 0 AND match_score <= 100
    ),
    fit_score numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        fit_score >= 0 AND fit_score <= 100
    ),
    intent_score numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        intent_score >= 0 AND intent_score <= 100
    ),
    risk_score numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        risk_score >= 0 AND risk_score <= 100
    ),
    status text NOT NULL DEFAULT 'new' CHECK (
        status IN (
            'new',
            'qualified',
            'contacted',
            'meeting',
            'won',
            'lost',
            'rejected'
        )
    ),
    rationale text,
    evidence jsonb NOT NULL DEFAULT '[]'::jsonb,
    owner_email text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS gold_matches_unique_idx
ON gold.matches (
    supplier_account_id,
    buyer_account_id,
    COALESCE(product_id, '00000000-0000-0000-0000-000000000000'::uuid)
);

CREATE INDEX IF NOT EXISTS gold_matches_supplier_idx
ON gold.matches(supplier_account_id);

CREATE INDEX IF NOT EXISTS gold_matches_buyer_idx
ON gold.matches(buyer_account_id);

CREATE INDEX IF NOT EXISTS gold_matches_score_idx
ON gold.matches(match_score DESC);

CREATE INDEX IF NOT EXISTS gold_matches_status_idx
ON gold.matches(status);

CREATE TABLE IF NOT EXISTS gold.account_360 (
    account_id uuid PRIMARY KEY REFERENCES silver.accounts(id) ON DELETE CASCADE,
    total_signals integer NOT NULL DEFAULT 0,
    last_signal_at timestamptz,
    latest_intent_score numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        latest_intent_score >= 0 AND latest_intent_score <= 100
    ),
    match_score numeric(5,2) NOT NULL DEFAULT 0 CHECK (
        match_score >= 0 AND match_score <= 100
    ),
    recommended_action text,
    next_best_touch text,
    estimated_annual_value numeric(16,2),
    pipeline_stage text,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.outreach_tasks (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id uuid REFERENCES gold.matches(id) ON DELETE SET NULL,
    account_id uuid NOT NULL REFERENCES silver.accounts(id) ON DELETE CASCADE,
    contact_id uuid REFERENCES silver.contacts(id) ON DELETE SET NULL,
    channel text NOT NULL CHECK (
        channel IN (
            'email',
            'linkedin',
            'phone',
            'whatsapp',
            'event',
            'manual'
        )
    ),
    template_key text,
    subject text,
    body text,
    status text NOT NULL DEFAULT 'draft' CHECK (
        status IN (
            'draft',
            'scheduled',
            'sent',
            'opened',
            'replied',
            'bounced',
            'failed',
            'completed'
        )
    ),
    due_at timestamptz,
    sent_at timestamptz,
    completed_at timestamptz,
    result_note text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS gold_outreach_tasks_account_idx
ON gold.outreach_tasks(account_id);

CREATE INDEX IF NOT EXISTS gold_outreach_tasks_match_idx
ON gold.outreach_tasks(match_id);

CREATE INDEX IF NOT EXISTS gold_outreach_tasks_status_idx
ON gold.outreach_tasks(status);

CREATE TABLE IF NOT EXISTS gold.kpis_daily (
    metric_date date PRIMARY KEY,
    qualified_matches integer NOT NULL DEFAULT 0,
    signals_ingested integer NOT NULL DEFAULT 0,
    outreach_sent integer NOT NULL DEFAULT 0,
    replies integer NOT NULL DEFAULT 0,
    meetings integer NOT NULL DEFAULT 0,
    pilot_accounts integer NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

-- ============================================================
-- UPDATED_AT TRIGGERS
-- ============================================================

DROP TRIGGER IF EXISTS silver_accounts_updated_at_trigger
ON silver.accounts;

CREATE TRIGGER silver_accounts_updated_at_trigger
BEFORE UPDATE ON silver.accounts
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS silver_contacts_updated_at_trigger
ON silver.contacts;

CREATE TRIGGER silver_contacts_updated_at_trigger
BEFORE UPDATE ON silver.contacts
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS silver_products_updated_at_trigger
ON silver.products;

CREATE TRIGGER silver_products_updated_at_trigger
BEFORE UPDATE ON silver.products
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS silver_signals_updated_at_trigger
ON silver.signals;

CREATE TRIGGER silver_signals_updated_at_trigger
BEFORE UPDATE ON silver.signals
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS silver_capabilities_updated_at_trigger
ON silver.capabilities;

CREATE TRIGGER silver_capabilities_updated_at_trigger
BEFORE UPDATE ON silver.capabilities
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS gold_matches_updated_at_trigger
ON gold.matches;

CREATE TRIGGER gold_matches_updated_at_trigger
BEFORE UPDATE ON gold.matches
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS gold_account_360_updated_at_trigger
ON gold.account_360;

CREATE TRIGGER gold_account_360_updated_at_trigger
BEFORE UPDATE ON gold.account_360
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS gold_outreach_tasks_updated_at_trigger
ON gold.outreach_tasks;

CREATE TRIGGER gold_outreach_tasks_updated_at_trigger
BEFORE UPDATE ON gold.outreach_tasks
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

DROP TRIGGER IF EXISTS gold_kpis_daily_updated_at_trigger
ON gold.kpis_daily;

CREATE TRIGGER gold_kpis_daily_updated_at_trigger
BEFORE UPDATE ON gold.kpis_daily
FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
```

---

## 1.5 MINIMUM SEED DATA MODEL

The demo database must contain:

### Supplier

```text
Butler's Leather
Country: India
City: Chennai
Products:
- Finished cow leather
- Finished goat leather
HS codes:
- 4107
- 4113
Certifications:
- REACH compliance
- ISO 9001, if true
- LWG, if true
Export target:
- Germany
- Europe
```

### Five Buyer Dossiers

```text
1. Picard
2. Roeckl
3. Bader
4. Kilger
5. Otto Schumacher
```

Each buyer must have:

- Company profile
- Country
- Product category
- Likely leather requirement
- Evidence source
- Contact role
- Signal type
- Match score
- Fit rationale
- Risk note
- Recommended next action

Do not present unverified emails as real. If contact emails are not verified, label them as:

```text
Contact pending verification
```

For the paid pilot, every delivered match must include a verified reachable contact or a verified sourcing pathway.

---

## 1.6 SEED SQL TEMPLATE

Use this as the base seed structure. Replace placeholder domains, emails, and evidence with verified data before the customer demo.

```sql
-- ============================================================
-- SEED SUPPLIER: BUTLER'S LEATHER
-- ============================================================

INSERT INTO silver.accounts (
    account_key,
    name,
    domain,
    country,
    region,
    industry,
    sub_industry,
    hq_city,
    website,
    import_hs_codes,
    product_categories,
    compliance_requirements,
    employee_range,
    status
) VALUES (
    'butlers-leather',
    'Butler''s Leather',
    'butlersleather.example',
    'IN',
    'Asia',
    'Leather Manufacturing',
    'Finished Leather Export',
    'Chennai',
    'https://butlersleather.example',
    ARRAY['4107','4113'],
    ARRAY['finished_cow_leather','finished_goat_leather'],
    ARRAY['REACH','ISO 9001'],
    '51-200',
    'active'
)
ON CONFLICT (account_key) DO UPDATE SET
    name = EXCLUDED.name,
    domain = EXCLUDED.domain,
    country = EXCLUDED.country,
    region = EXCLUDED.region,
    industry = EXCLUDED.industry,
    sub_industry = EXCLUDED.sub_industry,
    hq_city = EXCLUDED.hq_city,
    website = EXCLUDED.website,
    import_hs_codes = EXCLUDED.import_hs_codes,
    product_categories = EXCLUDED.product_categories,
    compliance_requirements = EXCLUDED.compliance_requirements,
    employee_range = EXCLUDED.employee_range,
    status = EXCLUDED.status;

-- ============================================================
-- SEED BUYER ACCOUNTS
-- Replace placeholder data with verified dossier data
-- ============================================================

INSERT INTO silver.accounts (
    account_key,
    name,
    domain,
    country,
    region,
    industry,
    sub_industry,
    hq_city,
    website,
    import_hs_codes,
    product_categories,
    compliance_requirements,
    employee_range,
    status
) VALUES
(
    'picard',
    'Picard',
    'picard.example',
    'DE',
    'EU',
    'Fashion Accessories',
    'Leather Goods',
    'Germany',
    'https://picard.example',
    ARRAY['4107','4113'],
    ARRAY['handbags','small_leather_goods'],
    ARRAY['REACH','LWG'],
    '201-500',
    'prospect'
),
(
    'roeckl',
    'Roeckl',
    'roeckl.example',
    'DE',
    'EU',
    'Fashion Accessories',
    'Gloves and Leather Accessories',
    'Germany',
    'https://roeckl.example',
    ARRAY['4107','4113'],
    ARRAY['gloves','leather_accessories'],
    ARRAY['REACH'],
    '201-500',
    'prospect'
),
(
    'bader',
    'Bader',
    'bader.example',
    'DE',
    'EU',
    'Leather Goods / Accessories',
    'Leather Product Manufacturing',
    'Germany',
    'https://bader.example',
    ARRAY['4107','4113'],
    ARRAY['leather_goods','accessories'],
    ARRAY['REACH'],
    '51-200',
    'prospect'
),
(
    'kilger',
    'Kilger',
    'kilger.example',
    'DE',
    'EU',
    'Leather Goods',
    'Leather Accessories',
    'Germany',
    'https://kilger.example',
    ARRAY['4107','4113'],
    ARRAY['leather_accessories'],
    ARRAY['REACH'],
    '11-50',
    'prospect'
),
(
    'otto-schumacher',
    'Otto Schumacher',
    'otto-schumacher.example',
    'DE',
    'EU',
    'Leather Goods',
    'Leather Accessories',
    'Germany',
    'https://otto-schumacher.example',
    ARRAY['4107','4113'],
    ARRAY['leather_goods','accessories'],
    ARRAY['REACH'],
    '11-50',
    'prospect'
)
ON CONFLICT (account_key) DO UPDATE SET
    name = EXCLUDED.name,
    domain = EXCLUDED.domain,
    country = EXCLUDED.country,
    region = EXCLUDED.region,
    industry = EXCLUDED.industry,
    sub_industry = EXCLUDED.sub_industry,
    hq_city = EXCLUDED.hq_city,
    website = EXCLUDED.website,
    import_hs_codes = EXCLUDED.import_hs_codes,
    product_categories = EXCLUDED.product_categories,
    compliance_requirements = EXCLUDED.compliance_requirements,
    employee_range = EXCLUDED.employee_range,
    status = EXCLUDED.status;
```

---

## 1.7 FASTAPI ENDPOINT CONTRACTS

The MVP API must expose these endpoints:

```text
GET  /api/v1/health
GET  /api/v1/matches
GET  /api/v1/signals
GET  /api/v1/accounts/{id}
POST /api/v1/outreach
```

Optional but recommended:

```text
POST /api/v1/matches/generate
GET  /api/v1/outreach
PATCH /api/v1/outreach/{id}
```

For the prototype, implement the five required endpoints first.

---

## 1.8 COMMON API CONVENTIONS

Base URL:

```text
http://localhost:8000/api/v1
```

Content type:

```text
application/json
```

Error format:

```json
{
  "error": {
    "code": "not_found",
    "message": "Account not found",
    "detail": {}
  }
}
```

Pagination format:

```json
{
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 5,
    "total_pages": 1
  }
}
```

---

## 1.9 ENDPOINT: HEALTH

### Route

```text
GET /api/v1/health
```

### Purpose

Verify API and database connectivity.

### Response 200

```json
{
  "status": "ok",
  "service": "trade-os-api",
  "version": "0.1.0",
  "db": "up",
  "timestamp": "2026-01-01T09:00:00Z"
}
```

### Response 503

```json
{
  "status": "degraded",
  "service": "trade-os-api",
  "version": "0.1.0",
  "db": "down",
  "timestamp": "2026-01-01T09:00:00Z"
}
```

---

## 1.10 ENDPOINT: MATCHES

### Route

```text
GET /api/v1/matches
```

### Purpose

Return ranked buyer matches for Butler’s Leather.

### Query Parameters

| Parameter | Type | Required | Default | Notes |
|---|---:|---|---:|---|
| `supplier_account_key` | string | no | `butlers-leather` | MVP assumes single supplier |
| `buyer_country` | string | no | null | Example: `DE` |
| `min_score` | number | no | 0 | 0 to 100 |
| `status` | string | no | null | `new`, `qualified`, `contacted`, etc. |
| `q` | string | no | null | Search buyer name |
| `page` | integer | no | 1 | |
| `page_size` | integer | no | 20 | Max 100 |
| `sort` | string | no | `-match_score` | Use `-match_score` or `-intent_score` |

### Response 200

```json
{
  "matches": [
    {
      "id": "8f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a11",
      "supplier_account_id": "1f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a01",
      "buyer": {
        "id": "2f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a02",
        "account_key": "picard",
        "name": "Picard",
        "country": "DE",
        "region": "EU",
        "domain": "picard.example",
        "industry": "Fashion Accessories",
        "sub_industry": "Leather Goods",
        "website": "https://picard.example"
      },
      "product": {
        "id": "3f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a03",
        "name": "Finished Cow Leather for Handbags",
        "material": "Cow",
        "hs_code": "4107",
        "color": "Brown/Black",
        "thickness_min_mm": 1.2,
        "thickness_max_mm": 1.6
      },
      "scores": {
        "overall": 92.5,
        "fit": 95.0,
        "intent": 88.0,
        "risk": 12.0
      },
      "status": "qualified",
      "rationale": "Picard matches Butler's Leather because it produces leather goods in Germany, likely sources finished leather, and has a product fit for cow leather in handbag/accessory lines.",
      "evidence": [
        {
          "type": "signal",
          "title": "Leather goods collection expansion",
          "url": "https://example.com/picard-news",
          "published_at": "2026-01-01T08:00:00Z",
          "snippet": "Company announces expanded leather accessory line."
        }
      ],
      "recommended_action": "Send intro email to sourcing/procurement contact with cow leather swatch card and REACH compliance summary.",
      "created_at": "2026-01-01T09:00:00Z",
      "updated_at": "2026-01-01T09:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 5,
    "total_pages": 1
  }
}
```

### Error Responses

```text
400 Bad Request
404 Supplier Not Found
500 Internal Server Error
```

---

## 1.11 ENDPOINT: SIGNALS

### Route

```text
GET /api/v1/signals
```

### Purpose

Return live or seeded buying signals.

### Query Parameters

| Parameter | Type | Required | Default | Notes |
|---|---:|---|---:|---|
| `account_id` | uuid | no | null | Filter by account |
| `account_key` | string | no | null | Alternative to account_id |
| `signal_type` | string | no | null | Example: `buying_intent` |
| `since` | ISO date | no | null | |
| `until` | ISO date | no | null | |
| `min_score` | number | no | 0 | |
| `q` | string | no | null | Search title/snippet |
| `page` | integer | no | 1 | |
| `page_size` | integer | no | 20 | |

### Response 200

```json
{
  "signals": [
    {
      "id": "9f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a21",
      "account": {
        "id": "2f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a02",
        "account_key": "picard",
        "name": "Picard",
        "country": "DE"
      },
      "signal_type": "buying_intent",
      "title": "Picard expands leather goods line",
      "url": "https://example.com/picard-news",
      "snippet": "The company is expanding its leather accessory collection.",
      "published_at": "2026-01-01T08:00:00Z",
      "score": 88.0,
      "entity": {
        "materials": ["cow leather", "goat leather"],
        "product_categories": ["handbags", "small leather goods"],
        "geography": ["DE", "EU"]
      },
      "created_at": "2026-01-01T09:00:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 10,
    "total_pages": 1
  }
}
```

---

## 1.12 ENDPOINT: ACCOUNT 360

### Route

```text
GET /api/v1/accounts/{id}
```

`id` can be a UUID or an `account_key` if implemented with a resolver.

### Purpose

Return full account dossier for one buyer.

### Response 200

```json
{
  "account": {
    "id": "2f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a02",
    "account_key": "picard",
    "name": "Picard",
    "domain": "picard.example",
    "country": "DE",
    "region": "EU",
    "industry": "Fashion Accessories",
    "sub_industry": "Leather Goods",
    "hq_city": "Germany",
    "website": "https://picard.example",
    "linkedin_url": null,
    "import_hs_codes": ["4107", "4113"],
    "product_categories": ["handbags", "small_leather_goods"],
    "compliance_requirements": ["REACH", "LWG"],
    "employee_range": "201-500",
    "status": "prospect",
    "created_at": "2026-01-01T09:00:00Z",
    "updated_at": "2026-01-01T09:00:00Z"
  },
  "contacts": [
    {
      "id": "4f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a04",
      "full_name": "Sourcing Contact",
      "title": "Head of Sourcing",
      "email": null,
      "phone": null,
      "linkedin_url": null,
      "is_primary": true,
      "confidence": 0.7
    }
  ],
  "products": [
    {
      "id": "3f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a03",
      "product_type": "buyer_requirement",
      "name": "Finished Cow Leather for Handbags",
      "material": "Cow",
      "hs_code": "4107",
      "color": "Brown/Black",
      "thickness_min_mm": 1.2,
      "thickness_max_mm": 1.6,
      "moq_sqft": 5000,
      "target_price": null,
      "currency": "EUR",
      "certification": ["REACH"]
    }
  ],
  "signals": [
    {
      "id": "9f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a21",
      "signal_type": "buying_intent",
      "title": "Picard expands leather goods line",
      "url": "https://example.com/picard-news",
      "snippet": "The company is expanding its leather accessory collection.",
      "published_at": "2026-01-01T08:00:00Z",
      "score": 88.0
    }
  ],
  "matches": [
    {
      "id": "8f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a11",
      "match_score": 92.5,
      "fit_score": 95.0,
      "intent_score": 88.0,
      "risk_score": 12.0,
      "status": "qualified",
      "rationale": "Picard matches Butler's Leather because it produces leather goods in Germany and likely sources finished leather."
    }
  ],
  "account_360": {
    "account_id": "2f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a02",
    "total_signals": 3,
    "last_signal_at": "2026-01-01T08:00:00Z",
    "latest_intent_score": 88.0,
    "match_score": 92.5,
    "recommended_action": "Send intro email with swatch card and REACH compliance summary.",
    "next_best_touch": "Email Head of Sourcing",
    "estimated_annual_value": 250000,
    "pipeline_stage": "qualified",
    "updated_at": "2026-01-01T09:00:00Z"
  },
  "outreach_tasks": []
}
```

### Error Response

```text
404 Account Not Found
```

---

## 1.13 ENDPOINT: OUTREACH

### Route

```text
POST /api/v1/outreach
```

### Purpose

Create a one-click outreach task or draft.

### Request Body

```json
{
  "match_id": "8f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a11",
  "account_id": "2f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a02",
  "contact_id": "4f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a04",
  "channel": "email",
  "template_key": "pilot_intro",
  "subject": "Finished cow leather supply for Picard leather goods",
  "body": "Hello, Butler's Leather is a Chennai-based exporter of finished cow and goat leather...",
  "due_at": "2026-01-02T10:00:00Z"
}
```

### Validation Rules

| Field | Rule |
|---|---|
| `account_id` | Required |
| `channel` | Required |
| `match_id` | Optional but recommended |
| `contact_id` | Required if channel is `email` and contact email exists |
| `template_key` | Optional |
| `subject` | Optional if template exists |
| `body` | Optional if template exists |

### Response 201

```json
{
  "outreach_task": {
    "id": "5f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a05",
    "match_id": "8f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a11",
    "account_id": "2f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a02",
    "contact_id": "4f2c1c8e-8f1f-4c1e-9d3b-2f8f6f9f1a04",
    "channel": "email",
    "template_key": "pilot_intro",
    "subject": "Finished cow leather supply for Picard leather goods",
    "body": "Hello, Butler's Leather is a Chennai-based exporter...",
    "status": "draft",
    "due_at": "2026-01-02T10:00:00Z",
    "sent_at": null,
    "completed_at": null,
    "result_note": null,
    "created_at": "2026-01-01T09:00:00Z",
    "updated_at": "2026-01-01T09:00:00Z"
  }
}
```

### Error Responses

```text
400 Validation Error
404 Account/Contact/Match Not Found
500 Internal Server Error
```

---

## 1.14 REACT COMPONENT TREE FOR THE 3 CORE VIEWS

The frontend has three primary views:

```text
1. Match Portal
2. Live Signals Feed
3. Account 360 & 1-Click Action
```

Use React Router.

### Route Map

```tsx
/                     → Redirect to /matches
/matches              → Match Portal
/signals              → Live Signals Feed
/accounts/:accountId  → Account 360
/outreach             → Optional outreach task list
```

---

## 1.15 APP COMPONENT TREE

```text
<App>
  <ErrorBoundary>
    <QueryClientProvider>
      <ToastProvider>
        <AppShell>
          <Sidebar />
          <Topbar />
          <Routes>
            <Route path="/matches" element={<MatchPortalPage />} />
            <Route path="/signals" element={<LiveSignalsFeedPage />} />
            <Route path="/accounts/:accountId" element={<Account360Page />} />
            <Route path="/outreach" element={<OutreachTaskTable />} />
          </Routes>
        </AppShell>
      </ToastProvider>
    </QueryClientProvider>
  </ErrorBoundary>
</App>
```

---

## 1.16 MATCH PORTAL COMPONENT TREE

Route:

```text
/matches
```

Component tree:

```text
<MatchPortalPage>
  <PageHeader
    title="Qualified Buyer Matches"
    subtitle="Germany/Europe — Finished Cow/Goat Leather"
  />

  <MatchFilterBar>
    <CountrySelect />
    <ScoreFilter />
    <StatusFilter />
    <SearchInput />
  </MatchFilterBar>

  <MatchTable>
    <MatchTableRow>
      <BuyerCell />
      <ProductFitCell />
      <ScoreBadge />
      <SignalBadge />
      <StatusBadge />
      <ActionCell />
    </MatchTableRow>
  </MatchTable>

  <MatchDrawer>
    <MatchScorePanel />
    <MatchRationale />
    <MatchEvidenceList />
    <MatchActionBar>
      <OpenAccount360Button />
      <CreateOutreachButton />
    </MatchActionBar>
  </MatchDrawer>
</MatchPortalPage>
```

### Match Portal UI Requirements

The Match Portal must show:

- Buyer name
- Country flag
- Product fit
- Overall score
- Fit score
- Intent score
- Risk score
- Latest signal
- Status
- One-click action

Each row should open a drawer with:

- Why this buyer matches
- Evidence links
- Product requirement
- Recommended outreach
- Button to open Account 360
- Button to create outreach

---

## 1.17 LIVE SIGNALS FEED COMPONENT TREE

Route:

```text
/signals
```

Component tree:

```text
<LiveSignalsFeedPage>
  <PageHeader
    title="Live Signals Feed"
    subtitle="Buying intent, expansion, product launches, regulatory changes"
  />

  <SignalFilterBar>
    <SignalTypeSelect />
    <AccountFilter />
    <DateRangeFilter />
    <ScoreFilter />
  </SignalFilterBar>

  <SignalStream>
    <SignalCard>
      <SignalSourceBadge />
      <SignalTitle />
      <SignalSnippet />
      <SignalEntityTags />
      <SignalScoreBadge />
      <OpenAccountButton />
    </SignalCard>
  </SignalStream>

  <SignalDetailDrawer>
    <SignalMetadata />
    <SignalEntityList />
    <SignalEvidenceLink />
    <CreateOutreachButton />
  </SignalDetailDrawer>
</LiveSignalsFeedPage>
```

### Signals Feed UI Requirements

Each signal card must show:

- Source
- Signal type
- Account name
- Published date
- Score
- Entity tags
- Snippet
- Button to open account

The signal detail drawer must show:

- Full snippet
- Evidence URL
- Related materials
- Related product categories
- Recommended action

---

## 1.18 ACCOUNT 360 & 1-CLICK ACTION COMPONENT TREE

Route:

```text
/accounts/:accountId
```

Component tree:

```text
<Account360Page>
  <AccountHeader>
    <AccountName />
    <CountryBadge />
    <IndustryBadge />
    <WebsiteLink />
    <LinkedInLink />
    <AccountScoreGauge />
  </AccountHeader>

  <AccountTabs>
    <Tab label="Overview">
      <AccountOverviewPanel>
        <MatchScorePanel />
        <IntentScorePanel />
        <RiskPanel />
        <RecommendedActionPanel />
        <EstimatedValuePanel />
      </AccountOverviewPanel>
    </Tab>

    <Tab label="Signals">
      <AccountSignalsPanel>
        <SignalCard />
      </AccountSignalsPanel>
    </Tab>

    <Tab label="Contacts">
      <AccountContactsPanel>
        <ContactTable />
      </AccountContactsPanel>
    </Tab>

    <Tab label="Products">
      <AccountProductsPanel>
        <ProductRequirementTable />
      </AccountProductsPanel>
    </Tab>

    <Tab label="Outreach">
      <AccountOutreachPanel>
        <OutreachTaskTable />
      </AccountOutreachPanel>
    </Tab>
  </AccountTabs>

  <OneClickActionPanel>
    <CreateEmailDraftButton />
    <CreateLinkedInTaskButton />
    <ScheduleFollowUpButton />
  </OneClickActionPanel>

  <OutreachComposerDialog>
    <OutreachTemplateSelector />
    <OutreachPreview />
    <CopyToClipboardButton />
    <SaveAsDraftButton />
  </OutreachComposerDialog>
</Account360Page>
```

### Account 360 UI Requirements

The Account 360 page must answer:

- Who is this buyer?
- Why are they relevant?
- What signals exist?
- What product fits?
- Who should we contact?
- What is the next best action?
- What message should we send?
- What outreach task has been created?

---

# SECTION 2  
# 7-DAY DAY-BY-DAY EXECUTION SPRINT: CODE TO DEMO

This is a strict 7-day sprint.

The goal is not to build a perfect platform.

The goal is to build a working prototype that can:

1. Show five qualified buyer matches.
2. Show live signals.
3. Open an account dossier.
4. Create a one-click outreach task.
5. Support a $500 paid pilot conversation.

---

## DAY 1 — WORKSPACE, INFRASTRUCTURE, API SKELETON

### Daily Objective

Create the repository, local environment, Docker Compose, PostgreSQL database, and FastAPI skeleton.

### Exact Code/File Created

```text
Trade OS/
├── README.md
├── Makefile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── backend/
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── core/config.py
│   │   ├── core/logging.py
│   │   ├── db/session.py
│   │   ├── db/base.py
│   │   └── api/v1/endpoints/health.py
│   └── tests/test_health.py
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/main.tsx
│   ├── src/App.tsx
│   └── src/styles/globals.css
└── scripts/bootstrap.sh
```

### Key Backend Files

`backend/requirements.txt`

```text
fastapi
uvicorn[standard]
sqlalchemy
psycopg[binary]
pydantic-settings
alembic
httpx
pytest
```

`docker-compose.yml`

```yaml
version: "3.9"

services:
  db:
    image: postgres:16
    container_name: trade_os_db
    environment:
      POSTGRES_USER: tradeos
      POSTGRES_PASSWORD: tradeos
      POSTGRES_DB: tradeos
    ports:
      - "5432:5432"
    volumes:
      - tradeos_pgdata:/var/lib/postgresql/data

  api:
    build:
      context: ./backend
    container_name: trade_os_api
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+psycopg://tradeos:tradeos@db:5432/tradeos
    depends_on:
      - db

volumes:
  tradeos_pgdata:
```

### Database/Data Seed Action

```bash
docker compose up db -d
createdb tradeos
psql tradeos -c "SELECT 1;"
```

No seed data yet.

### Definition of Done

- `docker compose up db -d` works.
- PostgreSQL is reachable.
- FastAPI starts.
- `/api/v1/health` returns `status: ok`.
- Frontend starts with placeholder page.

### End-of-Day Deliverable

```text
Working local stack with health endpoint.
```

Verification:

```bash
curl http://localhost:8000/api/v1/health
```

Expected:

```json
{
  "status": "ok",
  "service": "trade-os-api",
  "version": "0.1.0",
  "db": "up"
}
```

---

## DAY 2 — DATABASE SCHEMA, MODELS, SEED FOUNDATION

### Daily Objective

Create the full PostgreSQL medallion schema and SQLAlchemy models.

### Exact Code/File Created

```text
backend/
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/0001_initial_trade_os_schema.py
├── app/
│   ├── models/bronze.py
│   ├── models/silver.py
│   ├── models/gold.py
│   ├── db/init_db.py
│   └── scripts/seed_db.py
```

### Database/Data Seed Action

Run DDL migration:

```bash
cd backend
alembic upgrade head
```

Or manually execute the DDL:

```bash
psql tradeos -f sql/trade_os_ddl.sql
```

Seed supplier:

```sql
INSERT INTO silver.accounts (
    account_key,
    name,
    domain,
    country,
    region,
    industry,
    sub_industry,
    hq_city,
    website,
    import_hs_codes,
    product_categories,
    compliance_requirements,
    employee_range,
    status
) VALUES (
    'butlers-leather',
    'Butler''s Leather',
    'butlersleather.example',
    'IN',
    'Asia',
    'Leather Manufacturing',
    'Finished Leather Export',
    'Chennai',
    'https://butlersleather.example',
    ARRAY['4107','4113'],
    ARRAY['finished_cow_leather','finished_goat_leather'],
    ARRAY['REACH','ISO 9001'],
    '51-200',
    'active'
)
ON CONFLICT (account_key) DO UPDATE SET
    name = EXCLUDED.name;
```

### Definition of Done

- All schemas exist.
- All tables exist.
- All indexes exist.
- Supplier account exists.
- No SQL errors.

### End-of-Day Deliverable

```text
Complete Trade OS database schema with Butler's Leather supplier record.
```

Verification:

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema IN ('bronze','silver','gold')
ORDER BY table_schema, table_name;
```

---

## DAY 3 — API CONTRACTS: MATCHES, SIGNALS, ACCOUNTS

### Daily Objective

Implement the three read APIs needed for the demo.

### Exact Code/File Created

```text
backend/app/
├── schemas/common.py
├── schemas/account.py
├── schemas/signal.py
├── schemas/match.py
├── services/match_service.py
├── services/signal_service.py
├── services/account_service.py
├── api/v1/endpoints/matches.py
├── api/v1/endpoints/signals.py
├── api/v1/endpoints/accounts.py
└── api/v1/router.py
```

### Database/Data Seed Action

Seed five buyer accounts:

```text
Picard
Roeckl
Bader
Kilger
Otto Schumacher
```

Seed one product requirement per buyer.

Seed one signal per buyer.

Seed one match per buyer.

Minimum SQL pattern:

```sql
INSERT INTO silver.signals (
    account_id,
    signal_type,
    title,
    url,
    snippet,
    published_at,
    score,
    entity
)
SELECT
    a.id,
    'buying_intent',
    'Demo buying intent signal',
    'https://example.com/demo-signal',
    'Company shows potential demand for finished leather.',
    now() - interval '3 days',
    85,
    '{"materials":["cow leather","goat leather"]}'::jsonb
FROM silver.accounts a
WHERE a.account_key IN (
    'picard',
    'roeckl',
    'bader',
    'kilger',
    'otto-schumacher'
);
```

### Definition of Done

- `/api/v1/matches` returns five matches.
- `/api/v1/signals` returns signals.
- `/api/v1/accounts/{id}` returns full account dossier.
- API responses match the contract.
- No 500 errors.

### End-of-Day Deliverable

```text
Working read APIs for Match Portal, Signals Feed, and Account 360.
```

Verification:

```bash
curl "http://localhost:8000/api/v1/matches?supplier_account_key=butlers-leather"
curl "http://localhost:8000/api/v1/signals"
curl "http://localhost:8000/api/v1/accounts/picard"
```

---

## DAY 4 — FRONTEND SHELL + MATCH PORTAL

### Daily Objective

Build the frontend app shell and Match Portal.

### Exact Code/File Created

```text
frontend/src/
├── api/client.ts
├── api/matches.ts
├── types/match.ts
├── hooks/useMatches.ts
├── components/layout/AppShell.tsx
├── components/layout/Sidebar.tsx
├── components/layout/Topbar.tsx
├── components/shared/ScoreBadge.tsx
├── components/shared/SignalBadge.tsx
├── features/matches/MatchPortalPage.tsx
├── features/matches/MatchFilterBar.tsx
├── features/matches/MatchTable.tsx
├── features/matches/MatchDrawer.tsx
├── features/matches/MatchRationale.tsx
├── features/matches/MatchEvidenceList.tsx
└── features/matches/MatchActionBar.tsx
```

### Database/Data Seed Action

No new seed required if Day 3 is complete.

Optional: improve match rationale text.

### Definition of Done

- Match Portal loads.
- Five buyer matches appear.
- Scores render.
- Drawer opens.
- Rationale and evidence appear.
- Button to open Account 360 exists.

### End-of-Day Deliverable

```text
Working Match Portal with five qualified buyer matches.
```

Verification:

```bash
npm run dev
```

Open:

```text
http://localhost:5173/matches
```

---

## DAY 5 — LIVE SIGNALS FEED + ACCOUNT 360

### Daily Objective

Build the Signals Feed and Account 360 page.

### Exact Code/File Created

```text
frontend/src/
├── api/signals.ts
├── api/accounts.ts
├── types/signal.ts
├── types/account.ts
├── hooks/useSignals.ts
├── hooks/useAccount.ts
├── features/signals/LiveSignalsFeedPage.tsx
├── features/signals/SignalFilterBar.tsx
├── features/signals/SignalStream.tsx
├── features/signals/SignalCard.tsx
├── features/signals/SignalDetailDrawer.tsx
├── features/accounts/Account360Page.tsx
├── features/accounts/AccountHeader.tsx
├── features/accounts/AccountTabs.tsx
├── features/accounts/AccountOverviewPanel.tsx
├── features/accounts/AccountSignalsPanel.tsx
├── features/accounts/AccountContactsPanel.tsx
├── features/accounts/AccountProductsPanel.tsx
└── features/accounts/AccountOutreachPanel.tsx
```

### Database/Data Seed Action

Ensure each buyer has:

```text
At least 2 signals
At least 1 product requirement
At least 1 contact role
At least 1 match
```

Recommended seed:

```text
Picard:
- buying_intent
- product_launch

Roeckl:
- buying_intent
- expansion

Bader:
- buying_intent
- hiring

Kilger:
- buying_intent
- event

Otto Schumacher:
- buying_intent
- news
```

### Definition of Done

- Signals Feed loads.
- Signal cards show source, score, account, snippet.
- Account 360 loads from match row.
- Account tabs work.
- Signals, contacts, products appear.

### End-of-Day Deliverable

```text
Working Signals Feed and Account 360 page.
```

Verification:

```text
http://localhost:5173/signals
http://localhost:5173/accounts/picard
```

---

## DAY 6 — OUTREACH ACTION, DEMO POLISH, VERIFICATION

### Daily Objective

Build one-click outreach and polish the demo experience.

### Exact Code/File Created

```text
backend/app/
├── schemas/outreach.py
├── services/outreach_service.py
└── api/v1/endpoints/outreach.py

frontend/src/
├── api/outreach.ts
├── types/outreach.ts
├── hooks/useOutreach.ts
├── features/accounts/OneClickActionPanel.tsx
├── features/accounts/OutreachComposerDialog.tsx
├── features/outreach/OutreachTemplateSelector.tsx
├── features/outreach/OutreachPreview.tsx
└── features/outreach/OutreachTaskTable.tsx
```

### Database/Data Seed Action

Seed outreach templates:

```text
pilot_intro
follow_up_no_reply
swatch_card_offer
meeting_request
compliance_summary
```

Example template:

```text
Template key: pilot_intro
Subject: Finished cow leather supply for {account_name}
Body:
Hello {contact_first_name},

I am writing from Butler's Leather, Chennai. We export finished cow and goat leather to Europe and can support {account_name} with REACH-compliant material for {product_category}.

Would you be open to reviewing our swatch card and technical specification sheet?

Best regards,
{sender_name}
Butler's Leather
```

### Definition of Done

- One-click action creates outreach task.
- Outreach task appears in database.
- Outreach preview shows message.
- Copy button works.
- Demo flow works end to end.

### End-of-Day Deliverable

```text
Complete demo loop:
Match → Signal → Account 360 → One-click outreach.
```

Verification:

```bash
curl -X POST http://localhost:8000/api/v1/outreach \
  -H "Content-Type: application/json" \
  -d '{
    "account_id": "ACCOUNT_UUID",
    "channel": "email",
    "template_key": "pilot_intro"
  }'
```

---

## DAY 7 — DEMO REHEARSAL, PILOT DOCUMENTS, FINAL QA

### Daily Objective

Prepare the commercial demo, verify the five buyer dossiers, and finalize the pilot offer.

### Exact Code/File Created

```text
docs/
├── demo_script.md
├── pilot_agreement.md
├── buyer_dossier_verification.md
└── objection_handling.md

scripts/
├── verify_demo.sh
└── seed_demo.sh
```

### Database/Data Seed Action

Run final verification query:

```sql
SELECT
    a.name,
    a.country,
    a.sub_industry,
    a.product_categories,
    a.compliance_requirements,
    COUNT(s.id) AS signal_count,
    COUNT(c.id) AS contact_count,
    COUNT(m.id) AS match_count
FROM silver.accounts a
LEFT JOIN silver.signals s ON s.account_id = a.id
LEFT JOIN silver.contacts c ON c.account_id = a.id
LEFT JOIN gold.matches m ON m.buyer_account_id = a.id
WHERE a.account_key IN (
    'picard',
    'roeckl',
    'bader',
    'kilger',
    'otto-schumacher'
)
GROUP BY a.id
ORDER BY a.name;
```

Expected:

```text
Each buyer:
- signal_count >= 2
- contact_count >= 1
- match_count >= 1
```

### Definition of Done

- All five buyer dossiers verified.
- Demo script rehearsed twice.
- Pilot agreement written.
- Refund criteria written.
- Objection handling prepared.
- No broken UI states.
- API latency under 500ms locally.

### End-of-Day Deliverable

```text
Sales-ready prototype and commercial pilot package.
```

---

# SECTION 3  
# COMMERCIAL VALIDATION & SALES DEMO REHEARSAL

---

## 3.1 PRE-DEMO VERIFICATION CHECKLIST

Before showing Trade OS to Butler’s Leather, verify the five buyer dossiers.

Do not demo unverified data as if it is live intelligence.

Use this checklist for each buyer:

| Check | Required |
|---|---|
| Company name verified | Yes |
| Country verified | Yes |
| Website/domain verified | Yes |
| Industry/sub-industry verified | Yes |
| Product category relevant to finished leather | Yes |
| Likely use of cow/goat leather | Yes |
| Evidence source captured | Yes |
| Evidence date within 90 days preferred | Yes |
| Contact role identified | Yes |
| Contact email or LinkedIn verified | Preferred |
| Compliance requirements identified | Preferred |
| Match rationale written | Yes |
| Risk note written | Yes |
| Recommended next action written | Yes |
| No duplicate account | Yes |

---

## 3.2 FIVE BUYER DOSSIER VERIFICATION TABLE

Use this table before the demo.

| Buyer | Country | Product Fit | Evidence Type | Evidence URL | Contact Role | Intent Score | Risk | Verified? |
|---|---:|---|---|---|---|---:|---|---|
| Picard | Germany | Handbags / leather goods | News / website / catalog | Required | Sourcing / Procurement | 85+ | Low/Medium | Yes/No |
| Roeckl | Germany | Gloves / leather accessories | News / website / catalog | Required | Sourcing / Product Development | 85+ | Low/Medium | Yes/No |
| Bader | Germany | Leather goods / accessories | Website / trade show / job post | Required | Purchasing / Managing Director | 80+ | Medium | Yes/No |
| Kilger | Germany | Leather accessories | Website / social / event | Required | Owner / Purchasing | 75+ | Medium | Yes/No |
| Otto Schumacher | Germany | Leather goods / accessories | Website / news / directory | Required | Owner / Sourcing | 75+ | Medium | Yes/No |

If any buyer cannot be verified, replace it with another qualified German/EU buyer before the demo.

---

## 3.3 BUYER DOSSIER STANDARD FORMAT

Each buyer dossier must contain:

```text
Buyer Name:
Country:
City:
Website:
Industry:
Sub-industry:
Product Categories:
Likely Leather Use:
Likely HS Codes:
Compliance Requirements:
Company Size:
Signal Type:
Signal Evidence:
Signal Date:
Contact Role:
Contact Source:
Match Score:
Fit Score:
Intent Score:
Risk Score:
Rationale:
Risk Note:
Recommended Action:
Outreach Template:
```

---

## 3.4 15-MINUTE LIVE SALES DEMO SCRIPT

Audience:

```text
CEO / Export Director
Butler's Leather, Chennai
```

Goal:

```text
Sell the $500 paid pilot.
```

---

### MINUTE 0:00 — 1:30  
### OPENING HOOK

Say:

> “Thank you for your time. I am not going to show you a generic lead list. What I built is a buyer intelligence system specifically for Butler’s Leather.  
>   
> The goal is simple: identify five qualified German or European buyers for your finished cow and goat leather, show you why each one is relevant, and give you a ready-to-send outreach action for each account.  
>   
> This is not a database. It is a deal-flow engine.”

---

### MINUTE 1:30 — 3:00  
### BUSINESS PROBLEM

Say:

> “Exporters usually face three problems.  
>   
> First, buyer discovery is manual. You rely on trade fairs, directories, referrals, or random LinkedIn searches.  
>   
> Second, most leads are not qualified. You waste time on companies that do not actually import finished leather.  
>   
> Third, even when you find a good company, you do not know who to contact, what to say, or why they should respond.  
>   
> Trade OS solves these three problems by combining buyer matching, live signals, and one-click outreach.”

---

### MINUTE 3:00 — 6:00  
### DEMO: MATCH PORTAL

Open:

```text
/matches
```

Say:

> “This is the Match Portal. These are not raw leads. These are qualified matches for Butler’s Leather.  
>   
> Here you can see five buyers: Picard, Roeckl, Bader, Kilger, and Otto Schumacher.  
>   
> Each row shows the buyer, country, product fit, match score, intent score, risk score, and recommended action.  
>   
> Let’s open Picard.”

Click Picard.

Show:

- Match score
- Fit rationale
- Evidence
- Product requirement
- Recommended action

Say:

> “Picard is relevant because it operates in leather goods and likely sources finished leather for its product lines.  
>   
> The system shows the rationale, evidence, and the next action.  
>   
> This means your export team does not need to spend hours researching from scratch.”

---

### MINUTE 6:00 — 9:00  
### DEMO: LIVE SIGNALS FEED

Open:

```text
/signals
```

Say:

> “This is the Live Signals Feed.  
>   
> A signal is an event that suggests buying intent. It could be a product launch, expansion, hiring, trade show participation, regulatory change, or news about a leather product line.  
>   
> For example, if a German leather goods company announces a new collection, that is a signal that they may need material supply.  
>   
> Instead of contacting every company blindly, you contact the right company at the right time.”

Open one signal.

Show:

- Signal title
- Source
- Score
- Related account
- Entity tags

Say:

> “This is what makes Trade OS different. It does not just tell you who exists. It tells you who is showing signs of demand.”

---

### MINUTE 9:00 — 12:00  
### DEMO: ACCOUNT 360 + ONE-CLICK ACTION

Open:

```text
/accounts/picard
```

Say:

> “This is the Account 360 view.  
>   
> Here you see the full dossier: company profile, product fit, signals, contacts, outreach status, and recommended next action.  
>   
> The most important part is this one-click action.  
>   
> With one click, Trade OS creates an outreach draft using Butler’s Leather positioning, product details, and compliance information.”

Click:

```text
Create Email Draft
```

Show:

```text
Subject: Finished cow leather supply for Picard
Body: personalized intro message
```

Say:

> “Your team can review, edit, and send.  
>   
> The system removes the blank-page problem. It turns research into action.”

---

### MINUTE 12:00 — 13:30  
### ROI AND PILOT OFFER

Say:

> “The pilot is designed to be low-risk and outcome-based.  
>   
> For $500, we run a 14-day pilot.  
>   
> Our commitment is to deliver five qualified buyer matches for Butler’s Leather.  
>   
> Each qualified match will include:  
>   
> 1. A verified German or European company.  
> 2. A clear product fit for finished cow or goat leather.  
> 3. Evidence of relevance.  
> 4. A recommended contact path.  
> 5. A ready-to-use outreach message.  
>   
> If we do not deliver five qualified matches in 14 days, you receive a full refund based on the written criteria.”

---

### MINUTE 13:30 — 15:00  
### CLOSE

Say:

> “The next step is simple.  
>   
> We start with your product catalog, certifications, target countries, and ideal buyer profile.  
>   
> Within 14 days, you receive five qualified matches and outreach drafts.  
>   
> If you like the results, the pilot converts into a $950 monthly subscription.  
>   
> The $500 pilot fee is credited to your first month if you convert within seven days of pilot completion.  
>   
> Should we start with the pilot intake form today?”

---

## 3.5 EXACT CLOSING PITCH FOR THE $500 PAID PILOT

Use this exact pitch:

> “Mr./Ms. [Name], the pilot is $500 for 14 days.  
>   
> In that period, we will deliver five qualified buyer matches for Butler’s Leather.  
>   
> A qualified match means a German or European company that is relevant to finished cow or goat leather, has a documented product fit, includes evidence of relevance, identifies a recommended contact path, and comes with a ready-to-send outreach message.  
>   
> If we fail to deliver five qualified matches within 14 days, you receive a full refund under the written pilot terms.  
>   
> If you convert to the $950 monthly subscription within seven days of pilot completion, the $500 pilot fee is credited to your first month.  
>   
> The objective is not to sell you a tool. The objective is to create five real export opportunities.”

---

## 3.6 WRITTEN 14-DAY 5-MATCH REFUND CRITERIA

Include this in the pilot agreement.

### Pilot Deliverable

```text
Five qualified buyer matches within 14 calendar days.
```

### Qualified Match Definition

A qualified match must satisfy all five conditions:

1. **Geography**  
   The buyer is located in Germany or another approved European country.

2. **Product Fit**  
   The buyer is relevant to finished cow leather, finished goat leather, leather goods, leather accessories, or another category approved by Butler’s Leather.

3. **Evidence**  
   The match includes at least one evidence source, such as website, product catalog, news, trade show, job posting, regulatory signal, or company profile.

4. **Contact Path**  
   The match includes either:
   - A verified contact email, or
   - A verified LinkedIn profile, or
   - A verified sourcing/procurement pathway.

5. **Actionability**  
   The match includes a recommended outreach message and next action.

### Exclusions

The following do not count as qualified matches:

```text
Existing Butler's Leather customers
Companies with no plausible leather product fit
Duplicate companies
Companies with no evidence source
Companies outside approved geography
Contacts that are unverifiable or invalid
```

### Client Responsibilities

Butler’s Leather must provide within 48 hours:

```text
Product catalog or product summary
Target countries
Target buyer types
Certifications
Minimum order quantity
Pricing range, if comfortable sharing
Preferred contact person
Email domain and sender details
```

### Refund Terms

```text
If Trade OS does not deliver five qualified matches within 14 calendar days,
and the delay is not caused by Butler's Leather failing to provide required inputs,
the client receives a full refund of the $500 pilot fee.
```

### Conversion Terms

```text
If Butler's Leather converts to the $950/month subscription within seven days
of pilot completion, the $500 pilot fee is credited to the first invoice.
```

---

## 3.7 HANDLING THE 4 BIGGEST EXPORTER OBJECTIONS

---

### OBJECTION 1  
### “We already have buyers/agents.”

Response:

> “That is exactly why this is useful. Trade OS is not meant to replace your existing relationships. It is meant to show you the whitespace your current channels are missing.  
>   
> The pilot is low-risk: we deliver five new qualified matches. If they are duplicates of your existing buyers, they do not count. You only pay for new, qualified, actionable opportunities.”

Key point:

```text
Position Trade OS as whitespace discovery, not replacement.
```

---

### OBJECTION 2  
### “We can find this data ourselves.”

Response:

> “You can find names yourself. The problem is not names. The problem is qualification, timing, and outreach.  
>   
> Trade OS combines company fit, buying signals, evidence, contact path, and message generation. That saves your team days of research and increases the chance of getting a response.”

Key point:

```text
Sell workflow, not data.
```

---

### OBJECTION 3  
### “$500 is too much before seeing value.”

Response:

> “The $500 pilot is not a software fee. It is a paid discovery sprint.  
>   
> If we deliver five qualified matches, the cost is $100 per qualified match. If we fail, you get a refund under the written terms.  
>   
> Compared to the cost of one export sample shipment or one trade fair, this is a very small test.”

Key point:

```text
Anchor against cost of trade fair, samples, and sales time.
```

---

### OBJECTION 4  
### “We do not have time to use another tool.”

Response:

> “You do not need another tool to manage. The demo you just saw is the workflow.  
>   
> We deliver matches with rationale and outreach drafts. Your team only reviews and sends.  
>   
> In the pilot, we can also run the first outreach preparation with you so your team does not have to learn a system.”

Key point:

```text
Sell done-with-you execution, not software overhead.
```

---

# SECTION 4  
# FUTURE SCALING & POST-MVP ROADMAP

---

## 4.1 PHASE 2: WEEK 2–4  
### SCALING TO 3–5 DESIGN PARTNERS

After the Butler’s Leather pilot, expand to 3–5 design partners.

Target categories:

```text
1. Leather exporters
2. Chemical distributors supplying tanneries/leather manufacturers
3. Leather machinery vendors
4. Leather accessory manufacturers
5. Footwear component suppliers
```

Example design partners:

```text
- Chemical distributors such as Stahl or BASF-related distribution partners
- Leather machinery vendors
- Tannery chemical suppliers
- Finished leather exporters
- Leather goods manufacturers
```

Important: do not sell to large enterprises first. Sell to companies with a painful buyer-discovery problem and a short sales cycle.

---

## 4.2 DESIGN PARTNER OFFER

Use this structure:

```text
Design Partner Pilot
Price: $500 to $1,000
Duration: 14 to 21 days
Deliverable: 5 to 10 qualified matches
Incentive: 20% discount on first 3 months if converted
Requirement: Weekly feedback call
```

For chemical distributors:

```text
Target buyers:
- Tanneries
- Leather manufacturers
- Footwear manufacturers
- Leather goods manufacturers
- Chemical resellers
```

For machinery vendors:

```text
Target buyers:
- Tanneries
- Leather factories
- Footwear factories
- Leather goods manufacturers
- Small/mid-size manufacturing units
```

---

## 4.3 ONBOARDING NEW DESIGN PARTNERS

For each new design partner, complete this intake:

```text
1. Company profile
2. Product/service catalog
3. Target geography
4. Target buyer type
5. Ideal customer profile
6. Exclusions
7. Certifications
8. Sales cycle
9. Existing customers
10. Existing CRM/spreadsheet
11. Preferred outreach channel
12. Decision-maker titles
13. Success criteria
```

Then create a tenant-specific seed configuration:

```text
partner_config.json
product_catalog.json
target_geographies.json
buyer_personas.json
exclusion_list.json
outreach_templates.json
```

---

## 4.4 MULTI-TENANT PREPARATION

Before onboarding more than one paying customer, add tenant isolation.

Recommended schema change:

```sql
ALTER TABLE silver.accounts
ADD COLUMN organization_id uuid;

ALTER TABLE silver.contacts
ADD COLUMN organization_id uuid;

ALTER TABLE silver.products
ADD COLUMN organization_id uuid;

ALTER TABLE silver.signals
ADD COLUMN organization_id uuid;

ALTER TABLE gold.matches
ADD COLUMN organization_id uuid;

ALTER TABLE gold.outreach_tasks
ADD COLUMN organization_id uuid;
```

Long-term:

```text
Every row belongs to an organization.
Every API request is scoped by organization.
Every user belongs to an organization.
```

Do not overbuild multi-tenancy before the first pilot, but prepare for it.

---

## 4.5 TRANSITION FROM MANUAL SEED DATA TO AUTOMATED INGESTION

In Week 2–4, move from fully manual data to assisted automation.

Do not fully automate everything immediately.

Use this progression:

```text
Stage 1: Manual research + structured seed
Stage 2: Semi-automated scraping + human review
Stage 3: RSS/news ingestion + dedupe + human approval
Stage 4: Agent-assisted enrichment + human-in-the-loop
Stage 5: Autonomous ingestion with exception handling
```

---

## 4.6 AUTOMATED SOURCES

Potential sources:

```text
Company websites
Product catalogs
News pages
Press releases
RSS feeds
Trade show exhibitor lists
Industry directories
Job postings
LinkedIn company pages, where compliant
Customs/Bill of Lading data
Regulatory updates
Import/export databases
B2B marketplaces
```

Important compliance rules:

```text
Respect robots.txt
Respect rate limits
Do not scrape personal data unnecessarily
Use business contact data only where lawful
Comply with GDPR for EU contacts
Comply with CAN-SPAM/PECR for outreach
Maintain source attribution
Maintain data deletion process
```

---

## 4.7 INGESTION ARCHITECTURE

Add workers:

```text
backend/app/workers/
├── ingest_rss.py
├── ingest_webpages.py
├── ingest_customs.py
├── enrich_accounts.py
├── extract_signals.py
├── resolve_entities.py
└── generate_match_scores.py
```

Pipeline:

```text
Source
  ↓
Fetcher
  ↓
bronze.raw_sources
  ↓
Parser
  ↓
bronze.raw_accounts / bronze.raw_signals
  ↓
Entity Resolution
  ↓
silver.accounts / silver.signals
  ↓
Scoring
  ↓
gold.matches / gold.account_360
```

---

## 4.8 SIGNAL SCORING MODEL

Use a simple weighted score first.

```text
Signal Score =
  0.35 * source_quality
+ 0.25 * recency
+ 0.20 * material_fit
+ 0.10 * geography_fit
+ 0.10 * role_fit
```

Example:

```text
source_quality:
- official company news = 90
- trade show listing = 80
- job posting = 75
- news aggregator = 60
- social post = 50

recency:
- 0-7 days = 100
- 8-30 days = 80
- 31-90 days = 60
- 91-180 days = 30
- older = 10

material_fit:
- explicit cow/goat leather = 100
- leather goods = 80
- footwear = 70
- generic fashion = 40

geography_fit:
- Germany = 100
- EU = 90
- UK = 80
- other approved = 70
```

---

## 4.9 MATCH SCORING MODEL

Use this MVP formula:

```text
Match Score =
  0.40 * product_fit
+ 0.25 * intent_score
+ 0.15 * geography_fit
+ 0.10 * contact_quality
+ 0.10 * compliance_fit
```

Risk score should reduce priority but not necessarily disqualify.

```text
Risk factors:
- No verified contact
- Weak evidence
- Old signal
- Unclear product fit
- Sanctions/compliance issue
- Existing customer
- Duplicate account
```

---

## 4.10 PHASE 3: MONTH 2–3  
### ACTIVATING ENTERPRISE INTELLIGENCE

In Month 2–3, Trade OS becomes more than a match engine.

It becomes an enterprise intelligence platform.

Core additions:

```text
1. pgvector dense search
2. BM25/hybrid retrieval
3. Customs manifest data
4. Autonomous LangGraph agents
5. Enterprise packaging
```

---

## 4.11 PGVECTOR + HYBRID RETRIEVAL

Enable vector search for semantic matching.

Example use cases:

```text
Find companies similar to Picard
Find buyers whose product descriptions imply cow leather usage
Find signals semantically related to finished leather sourcing
Match unstructured catalog text to buyer requirements
```

Future DDL:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS silver.embeddings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type text NOT NULL CHECK (
        entity_type IN (
            'account',
            'contact',
            'product',
            'signal',
            'source'
        )
    ),
    entity_id uuid NOT NULL,
    model text NOT NULL,
    embedding vector(1536),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS silver_embeddings_entity_idx
ON silver.embeddings(entity_type, entity_id);

CREATE INDEX IF NOT EXISTS silver_embeddings_hnsw_idx
ON silver.embeddings
USING hnsw (embedding vector_cosine_ops);
```

For BM25-style lexical search, use PostgreSQL full-text search:

```sql
ALTER TABLE silver.signals
ADD COLUMN search_vector tsvector;

UPDATE silver.signals
SET search_vector = to_tsvector('english', coalesce(title,'') || ' ' || coalesce(snippet,''));

CREATE INDEX IF NOT EXISTS silver_signals_search_idx
ON silver.signals USING gin(search_vector);

CREATE OR REPLACE FUNCTION silver.signals_search_vector_update()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector = to_tsvector('english', coalesce(NEW.title,'') || ' ' || coalesce(NEW.snippet,''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS silver_signals_search_vector_trigger
ON silver.signals;

CREATE TRIGGER silver_signals_search_vector_trigger
BEFORE INSERT OR UPDATE ON silver.signals
FOR EACH ROW EXECUTE FUNCTION silver.signals_search_vector_update();
```

Hybrid retrieval pattern:

```text
Final Retrieval Score =
  0.60 * semantic_score
+ 0.40 * lexical_score
```

Where:

```text
semantic_score = pgvector cosine similarity
lexical_score = PostgreSQL ts_rank_cd or BM25-compatible rank
```

---

## 4.12 CUSTOMS MANIFEST / BILL OF LADING DATA FLOW

Customs data is one of the highest-value data sources for export intelligence.

Relevant HS codes:

```text
4107: Bovine leather further prepared after tanning
4113: Goat leather further prepared after tanning
```

Additional related codes may include:

```text
4104
4105
4106
4112
4114
4115
```

Use only codes relevant to Butler’s Leather.

---

## 4.13 CUSTOMS DATA SCHEMA

Future DDL:

```sql
CREATE TABLE IF NOT EXISTS bronze.raw_customs_shipments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id uuid REFERENCES bronze.raw_sources(id),
    bill_of_lading_number text,
    shipment_date date,
    origin_country text,
    destination_country text,
    shipper_name text,
    consignee_name text,
    notify_party_name text,
    hs_code text,
    goods_description text,
    quantity numeric,
    quantity_unit text,
    weight_kg numeric,
    vessel_name text,
    port_of_loading text,
    port_of_discharge text,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    ingested_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS silver.customs_shipments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id uuid REFERENCES silver.accounts(id),
    matched_consignee_name text,
    matched_shipper_name text,
    bill_of_lading_number text,
    shipment_date date,
    origin_country text,
    destination_country text,
    hs_code text,
    goods_description text,
    quantity numeric,
    quantity_unit text,
    weight_kg numeric,
    port_of_loading text,
    port_of_discharge text,
    confidence numeric(5,2),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.trade_lanes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_account_id uuid REFERENCES silver.accounts(id),
    buyer_account_id uuid REFERENCES silver.accounts(id),
    hs_code text,
    shipment_count integer NOT NULL DEFAULT 0,
    total_quantity numeric,
    total_weight_kg numeric,
    first_shipment_date date,
    last_shipment_date date,
    estimated_annual_value numeric,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
```

---

## 4.14 CUSTOMS INTELLIGENCE USE CASES

Use customs data to answer:

```text
Who is importing finished leather into Germany?
Which companies import from India?
Which consignees import HS 4107 or 4113?
Which buyers import repeatedly?
Which buyers changed suppliers?
Which buyers increased volume?
Which buyers are new to a category?
Which suppliers are competitors?
What is the estimated annual value of a trade lane?
```

This becomes a powerful enterprise feature.

---

## 4.15 AUTONOMOUS LANGGRAPH AGENT WORKFLOWS

In Month 2–3, introduce agent workflows.

Do not make agents fully autonomous without human review.

Use this model:

```text
Agent proposes
Human approves
System records evidence
```

---

## 4.16 AGENT ROLES

### Scout Agent

Purpose:

```text
Discover new sources, companies, and signals.
```

Inputs:

```text
Target geography
Target category
Target HS codes
Existing accounts
Exclusion list
```

Outputs:

```text
Candidate companies
Candidate URLs
Candidate signals
Source quality score
```

---

### Enricher Agent

Purpose:

```text
Extract structured fields from raw pages/documents.
```

Outputs:

```text
Company name
Domain
Country
Industry
Product categories
Materials
Certifications
Contact roles
Evidence snippet
```

---

### Resolver Agent

Purpose:

```text
Deduplicate and resolve entities.
```

Outputs:

```text
Canonical account_id
Duplicate confidence
Conflict flags
Merge recommendation
```

---

### Synthesizer Agent

Purpose:

```text
Create match rationale and outreach drafts.
```

Outputs:

```text
Match rationale
Risk note
Recommended action
Email subject
Email body
LinkedIn message
```

---

## 4.17 LANGGRAPH STATE DESIGN

Example state:

```python
class TradeOSAgentState(TypedDict):
    task_id: str
    organization_id: str
    supplier_profile: dict
    target_geographies: list[str]
    target_categories: list[str]
    candidate_accounts: list[dict]
    raw_signals: list[dict]
    enriched_accounts: list[dict]
    resolved_accounts: list[dict]
    matches: list[dict]
    outreach_drafts: list[dict]
    human_review_status: str
    errors: list[str]
```

Example graph:

```text
START
  ↓
Scout
  ↓
Enricher
  ↓
Resolver
  ↓
Synthesizer
  ↓
Human Review
  ↓
Persist to Gold
  ↓
END
```

---

## 4.18 AGENT GUARDRAILS

Required guardrails:

```text
No fabricated evidence
Every claim must have source attribution
No scraping behind authentication
No personal data beyond professional contact information
Rate limiting
Domain-level opt-out list
Human approval before match becomes qualified
Audit log for every agent action
Confidence threshold before publishing
```

---

## 4.19 ENTERPRISE TIER PACKAGING

Package the enterprise offer as:

```text
Trade OS Enterprise
$2,500/month
```

### Enterprise Features

```text
1. Up to 20 qualified matches per month
2. Live signal monitoring
3. Customs/Bill of Lading intelligence
4. Account 360 dossiers
5. Multi-user access
6. CRM export/integration
7. API access
8. Dedicated success manager
9. Weekly strategy call
10. Custom target markets
11. Competitor monitoring
12. Trade lane analytics
13. Outreach sequence support
14. SLA and priority support
```

### Enterprise Success Metrics

```text
Qualified matches delivered
Meetings booked
Pipeline value created
Response rate
Time to first meeting
Account coverage
Data accuracy
Customer retention
```

---

## 4.20 PRICING LADDER

Use this pricing ladder:

| Tier | Price | Deliverable | Target Customer |
|---|---:|---|---|
| Paid Pilot | $500 | 5 qualified matches in 14 days | Butler’s Leather |
| Growth | $950/month | 10 qualified matches/month, signals, outreach drafts | Single exporter/SMB |
| Enterprise | $2,500/month | 20+ matches, customs data, API, multi-user, success manager | Mid-size exporter/distributor |

---

## 4.21 REVENUE MODEL

First 90 days target:

```text
1 paid pilot: $500
3 design partners: $1,500 to $3,000
2 converted subscriptions: $1,900/month
1 enterprise pilot: $2,500/month potential
```

90-day revenue goal:

```text
$5,000 to $10,000 closed/piloted
$3,000 to $5,000 MRR pipeline
```

---

## 4.22 OPERATING CADENCE

### Weekly Customer Routine

For each paying customer:

```text
Monday:
- Refresh signals
- Review new matches
- Update account 360

Tuesday:
- Send top 2 outreach drafts

Wednesday:
- Follow up on sent outreach
- Update contact status

Thursday:
- Review replies
- Book meetings

Friday:
- Send weekly report
- Plan next week
```

### Weekly Internal Routine

```text
Monday:
- Data quality review

Tuesday:
- Match scoring review

Wednesday:
- Customer success calls

Thursday:
- Product improvements

Friday:
- Pipeline review and demo rehearsal
```

---

## 4.23 PRODUCT METRICS DASHBOARD

Track these metrics from Day 1:

```text
Number of qualified matches delivered
Number of matches accepted by client
Number of outreach drafts created
Number of outreach messages sent
Response rate
Meeting rate
Time to first qualified match
Time to first meeting
Pilot conversion rate
Monthly churn
Net revenue retention
```

---

## 4.24 RISK REGISTER

| Risk | Impact | Mitigation |
|---|---|---|
| Weak data quality | High | Human verification, evidence links, refund criteria |
| Fake/unverified contacts | High | Contact verification, LinkedIn/source validation |
| Overpromising automation | High | Sell pilot outcomes, not AI magic |
| GDPR/outreach compliance | High | Business-only data, opt-out, lawful basis, consent where needed |
| Scraping blocks | Medium | Use RSS, APIs, licensed data, manual research |
| Low pilot conversion | High | Define success criteria, weekly check-ins, fast value |
| Single-customer dependency | Medium | Add design partners in Week 2 |
| Scope creep | Medium | Freeze MVP to five endpoints and three views |

---

# 5. FINAL LAUNCH CHECKLIST

Before the Butler’s Leather demo, confirm:

## Technical Checklist

```text
PostgreSQL running
FastAPI running
React frontend running
/api/v1/health returns ok
/api/v1/matches returns five matches
/api/v1/signals returns signals
/api/v1/accounts/{id} returns account 360
/api/v1/outreach creates task
No console errors
No broken links
No empty states in demo path
Demo data seeded
Database backed up
```

## Commercial Checklist

```text
Five buyer dossiers verified
Evidence links verified
Contact roles verified
Match rationales written
Risk notes written
Outreach templates ready
Pilot agreement ready
Refund criteria written
Conversion offer ready
Objection handling rehearsed
Demo rehearsed twice
```

## Demo Checklist

```text
Match Portal opens instantly
Picard match opens cleanly
Signals Feed loads quickly
Account 360 loads without error
One-click outreach creates draft
Outreach preview looks professional
Score badges are readable
Evidence links are clickable
Recommended action is clear
Closing slide/offer is ready
```

---

# 6. FINAL EXECUTION PRINCIPLE

Trade OS must not be positioned as:

```text
Another database.
Another lead list.
Another AI dashboard.
```

It must be positioned as:

```text
A qualified export opportunity engine.
```

The prototype proves this by doing four things exceptionally well:

1. Show the right buyer.
2. Explain why now.
3. Provide the evidence.
4. Create the next action.

If the demo achieves that, the $500 pilot becomes easy to sell.

If the pilot delivers five qualified matches, the $950/month subscription becomes easy to justify.

If the platform then adds customs data, hybrid retrieval, and agent workflows, the $2,500/month Enterprise Tier becomes a natural expansion.