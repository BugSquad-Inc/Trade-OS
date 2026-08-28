import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. 001_extensions.sql
w("backend/sql/001_extensions.sql", """-- Trade OS Database Extensions
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
""")

# 2. 002_schemas.sql
w("backend/sql/002_schemas.sql", """-- Trade OS Schemas
CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS audit;
""")

# 3. 003_functions.sql
w("backend/sql/003_functions.sql", """-- Trade OS Utility Functions
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
""")

# 4. 004_bronze.sql
w("backend/sql/004_bronze.sql", """-- Bronze Schema: Raw Immutable Ingestion & Lineage
CREATE TABLE IF NOT EXISTS bronze.source_system (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL UNIQUE,
  kind TEXT NOT NULL CHECK (kind IN ('api','web','rss','file','manual','crm')),
  base_url TEXT,
  legal_basis TEXT,
  robots_policy TEXT,
  auth JSONB NOT NULL DEFAULT '{}',
  rate_limit JSONB NOT NULL DEFAULT '{"requests_per_minute": 30}',
  enabled BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS bronze.ingestion_run (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES bronze.source_system(id) ON DELETE CASCADE,
  status TEXT NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued','running','succeeded','failed','partial')),
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ,
  cursor TEXT,
  stats JSONB NOT NULL DEFAULT '{}',
  error TEXT
);

CREATE TABLE IF NOT EXISTS bronze.raw_document (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID NOT NULL REFERENCES bronze.source_system(id),
  external_id TEXT,
  url TEXT,
  title TEXT,
  language TEXT,
  mime_type TEXT,
  content_text TEXT,
  content_json JSONB,
  content_hash TEXT NOT NULL,
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  meta JSONB NOT NULL DEFAULT '{}',
  UNIQUE (source_id, external_id)
);

CREATE TABLE IF NOT EXISTS bronze.raw_extract (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  raw_document_id UUID NOT NULL REFERENCES bronze.raw_document(id) ON DELETE CASCADE,
  extractor_name TEXT NOT NULL,
  extractor_version TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'success' CHECK (status IN ('success','failed','partial')),
  payload JSONB NOT NULL DEFAULT '{}',
  confidence NUMERIC NOT NULL DEFAULT 0,
  error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
""")

# 5. 005_silver.sql
w("backend/sql/005_silver.sql", """-- Silver Schema: Canonical Entities, Normalization & Relationships
CREATE TABLE IF NOT EXISTS silver.entity_company (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  canonical_name TEXT NOT NULL,
  legal_name TEXT,
  domain TEXT,
  country_code CHAR(2) NOT NULL,
  city TEXT,
  region TEXT,
  postal_code TEXT,
  website TEXT,
  linkedin_url TEXT,
  segment TEXT NOT NULL DEFAULT 'Leather goods',
  description TEXT,
  founded_year INTEGER,
  employee_range TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','inactive','unknown','risk')),
  confidence NUMERIC NOT NULL DEFAULT 1.0,
  search_vector TSVECTOR,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS silver.entity_person (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID NOT NULL REFERENCES silver.entity_company(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  title TEXT,
  email TEXT,
  phone TEXT,
  linkedin_url TEXT,
  is_primary BOOLEAN NOT NULL DEFAULT false,
  confidence NUMERIC NOT NULL DEFAULT 0.8,
  verification_status TEXT NOT NULL DEFAULT 'illustrative' CHECK (verification_status IN ('verified','inferred','illustrative')),
  consent_status TEXT NOT NULL DEFAULT 'legitimate_interest' CHECK (consent_status IN ('legitimate_interest','consent','contract','none')),
  legal_basis TEXT NOT NULL DEFAULT 'B2B legitimate interest under GDPR Art. 6(1)(f)',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS silver.entity_product (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID NOT NULL REFERENCES silver.entity_company(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  hs_code TEXT,
  material_types JSONB NOT NULL DEFAULT '[]',
  tannage JSONB NOT NULL DEFAULT '[]',
  thickness_range_mm JSONB NOT NULL DEFAULT '[]',
  finish JSONB NOT NULL DEFAULT '[]',
  spec JSONB NOT NULL DEFAULT '{}',
  search_vector TSVECTOR,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS silver.entity_certification (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_id UUID NOT NULL REFERENCES silver.entity_company(id) ON DELETE CASCADE,
  certification_type TEXT NOT NULL,
  certification_name TEXT NOT NULL,
  issued_by TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','expired','pending','revoked')),
  valid_from DATE,
  valid_to DATE,
  evidence JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS silver.trade_lane_benchmark (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  origin_country CHAR(2) NOT NULL DEFAULT 'IN',
  origin_port TEXT NOT NULL DEFAULT 'INMAA',
  destination_country CHAR(2) NOT NULL DEFAULT 'DE',
  destination_port TEXT NOT NULL DEFAULT 'DEHAM',
  mode TEXT NOT NULL DEFAULT 'sea' CHECK (mode IN ('sea','air','multimodal')),
  container_type TEXT NOT NULL DEFAULT '40HC',
  rate_usd NUMERIC NOT NULL,
  rate_low_usd NUMERIC NOT NULL,
  rate_high_usd NUMERIC NOT NULL,
  transit_days_min INTEGER NOT NULL,
  transit_days_max INTEGER NOT NULL,
  port_congestion_index TEXT NOT NULL DEFAULT 'Normal (1.2 days wait)',
  reroute_risk_notes TEXT,
  effective_start DATE NOT NULL DEFAULT CURRENT_DATE,
  effective_end DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
""")

# 6. 006_gold.sql
w("backend/sql/006_gold.sql", """-- Gold Schema: Scores, Matches, Signals, Decision Outputs
CREATE TABLE IF NOT EXISTS gold.exporter_capability (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  company_name TEXT NOT NULL,
  location TEXT NOT NULL,
  cluster TEXT NOT NULL,
  export_market_focus JSONB NOT NULL DEFAULT '["Germany","EU"]',
  material_types JSONB NOT NULL DEFAULT '["finished bovine leather","goat nappa","crust"]',
  tannage JSONB NOT NULL DEFAULT '["vegetable","chrome","chrome-free"]',
  thickness_range_mm JSONB NOT NULL DEFAULT '["0.8-1.0","1.2-1.4","1.6-2.2"]',
  finish_capabilities JSONB NOT NULL DEFAULT '["aniline","semi-aniline","pigmented","pull-up"]',
  monthly_capacity_sqft INTEGER NOT NULL DEFAULT 50000,
  moq_sqft INTEGER NOT NULL DEFAULT 3000,
  lead_time_days INTEGER NOT NULL DEFAULT 35,
  sample_lead_time_days INTEGER NOT NULL DEFAULT 10,
  port_of_export TEXT NOT NULL DEFAULT 'Chennai Port (INMAA)',
  incoterms JSONB NOT NULL DEFAULT '["FOB","CIF","EXW"]',
  certifications JSONB NOT NULL DEFAULT '["LWG Gold","ISO 9001","ISO 14001","REACH"]',
  eudr_readiness_score INTEGER NOT NULL DEFAULT 68,
  eudr_gap_summary TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.match_profile (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  exporter_capability_id UUID REFERENCES gold.exporter_capability(id),
  objective TEXT NOT NULL DEFAULT 'find_buyers',
  criteria JSONB NOT NULL DEFAULT '{}',
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.match_candidate (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  match_profile_id UUID REFERENCES gold.match_profile(id) ON DELETE CASCADE,
  buyer_id UUID NOT NULL REFERENCES silver.entity_company(id) ON DELETE CASCADE,
  total_score NUMERIC(5,2) NOT NULL,
  product_fit_score NUMERIC(5,2) NOT NULL,
  compliance_score NUMERIC(5,2) NOT NULL,
  lane_economics_score NUMERIC(5,2) NOT NULL,
  intent_signals_score NUMERIC(5,2) NOT NULL,
  accessibility_score NUMERIC(5,2) NOT NULL,
  grade CHAR(1) NOT NULL CHECK (grade IN ('A','B','C','D')),
  rank INTEGER NOT NULL,
  score_version TEXT NOT NULL DEFAULT 'v1.0.0',
  drivers JSONB NOT NULL DEFAULT '[]',
  key_gaps JSONB NOT NULL DEFAULT '[]',
  next_best_action TEXT NOT NULL,
  outreach_angle TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'suggested' CHECK (status IN ('suggested','shortlisted','contacted','dismissed','converted')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (buyer_id)
);

CREATE TABLE IF NOT EXISTS gold.match_score_history (
  id BIGSERIAL PRIMARY KEY,
  buyer_id UUID NOT NULL REFERENCES silver.entity_company(id),
  score NUMERIC(5,2) NOT NULL,
  score_version TEXT NOT NULL,
  drivers JSONB NOT NULL,
  computed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.signal (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  entity_id UUID NOT NULL REFERENCES silver.entity_company(id) ON DELETE CASCADE,
  category TEXT NOT NULL CHECK (category IN ('regulatory','intent','logistics','market','compliance')),
  severity TEXT NOT NULL DEFAULT 'medium' CHECK (severity IN ('low','medium','high','critical')),
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  quote TEXT,
  source_url TEXT,
  detected_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  score NUMERIC NOT NULL DEFAULT 0,
  evidence JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.signal_evidence (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  signal_id UUID NOT NULL REFERENCES gold.signal(id) ON DELETE CASCADE,
  document_url TEXT,
  quote TEXT,
  confidence NUMERIC NOT NULL DEFAULT 0.9,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS gold.actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  buyer_id UUID NOT NULL REFERENCES silver.entity_company(id) ON DELETE CASCADE,
  action_type TEXT NOT NULL CHECK (action_type IN ('outreach_generation','crm_export','sample_request')),
  status TEXT NOT NULL DEFAULT 'generated',
  payload JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS audit.audit_event (
  id BIGSERIAL PRIMARY KEY,
  action TEXT NOT NULL,
  object_type TEXT NOT NULL,
  object_id TEXT,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
""")

# 7. 007_indexes.sql
w("backend/sql/007_indexes.sql", """-- Core Performance & Search Indexes
CREATE INDEX IF NOT EXISTS idx_company_country ON silver.entity_company(country_code);
CREATE INDEX IF NOT EXISTS idx_company_name_trgm ON silver.entity_company USING gin(canonical_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_company_search_vector ON silver.entity_company USING gin(search_vector);
CREATE INDEX IF NOT EXISTS idx_person_company ON silver.entity_person(company_id);
CREATE INDEX IF NOT EXISTS idx_product_company ON silver.entity_product(company_id);
CREATE INDEX IF NOT EXISTS idx_product_search_vector ON silver.entity_product USING gin(search_vector);
CREATE INDEX IF NOT EXISTS idx_signal_entity ON gold.signal(entity_id);
CREATE INDEX IF NOT EXISTS idx_signal_category ON gold.signal(category);
CREATE INDEX IF NOT EXISTS idx_signal_detected_at ON gold.signal(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_match_candidate_rank ON gold.match_candidate(rank);
CREATE INDEX IF NOT EXISTS idx_match_candidate_score ON gold.match_candidate(total_score DESC);
CREATE INDEX IF NOT EXISTS idx_score_history_buyer ON gold.match_score_history(buyer_id);
CREATE INDEX IF NOT EXISTS idx_audit_event_created ON audit.audit_event(created_at DESC);
""")

# 8. 008_triggers.sql
w("backend/sql/008_triggers.sql", """-- Triggers
DROP TRIGGER IF EXISTS entity_company_updated_at ON silver.entity_company;
CREATE TRIGGER entity_company_updated_at BEFORE UPDATE ON silver.entity_company FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS entity_person_updated_at ON silver.entity_person;
CREATE TRIGGER entity_person_updated_at BEFORE UPDATE ON silver.entity_person FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS entity_product_updated_at ON silver.entity_product;
CREATE TRIGGER entity_product_updated_at BEFORE UPDATE ON silver.entity_product FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trade_lane_benchmark_updated_at ON silver.trade_lane_benchmark;
CREATE TRIGGER trade_lane_benchmark_updated_at BEFORE UPDATE ON silver.trade_lane_benchmark FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS exporter_capability_updated_at ON gold.exporter_capability;
CREATE TRIGGER exporter_capability_updated_at BEFORE UPDATE ON gold.exporter_capability FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS match_candidate_updated_at ON gold.match_candidate;
CREATE TRIGGER match_candidate_updated_at BEFORE UPDATE ON gold.match_candidate FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- Full Text Search update triggers
DROP TRIGGER IF EXISTS entity_company_search_update ON silver.entity_company;
CREATE TRIGGER entity_company_search_update
BEFORE INSERT OR UPDATE ON silver.entity_company
FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger(
  search_vector, 'pg_catalog.english', canonical_name, segment, description
);

DROP TRIGGER IF EXISTS entity_product_search_update ON silver.entity_product;
CREATE TRIGGER entity_product_search_update
BEFORE INSERT OR UPDATE ON silver.entity_product
FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger(
  search_vector, 'pg_catalog.english', name, description, hs_code
);
""")

print("[SUCCESS] Part 2 (SQL DDL) built successfully")
