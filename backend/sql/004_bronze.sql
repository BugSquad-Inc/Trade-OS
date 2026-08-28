-- Bronze Schema: Raw Immutable Ingestion & Lineage
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
