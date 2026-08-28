-- Triggers
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
