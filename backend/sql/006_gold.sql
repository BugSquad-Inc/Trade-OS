-- Gold Schema: Scores, Matches, Signals, Decision Outputs
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
