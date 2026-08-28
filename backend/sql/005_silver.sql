-- Silver Schema: Canonical Entities, Normalization & Relationships
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
