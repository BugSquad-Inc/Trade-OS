-- Core Performance & Search Indexes
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
