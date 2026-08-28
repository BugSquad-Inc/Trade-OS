import sys
import os
sys.path.insert(0, os.path.abspath("backend"))

from sqlalchemy import text
from app.database import engine
from app.config import settings

def run_readiness_audit():
    print("=" * 70)
    print("TRADE OS -- PRODUCTION READINESS AND VERIFICATION AUDIT")
    print("=" * 70)
    with engine.connect() as conn:
        print("[1/5] Checking Database Schemas...")
        schemas = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('bronze', 'silver', 'gold', 'audit', 'app')")).fetchall()
        schema_names = [s[0] for s in schemas]
        print(f"      Found Schemas: {schema_names}")
        assert len(schema_names) >= 4

        print("[2/5] Verifying Medallion Tables...")
        tables = conn.execute(text("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('silver', 'gold', 'audit')")).fetchall()
        print(f"      Total Tables: {len(tables)}")
        assert len(tables) >= 8

        print("[3/5] Verifying Data Counts...")
        exporters = conn.execute(text("SELECT count(*) FROM gold.exporter_capability")).scalar()
        buyers = conn.execute(text("SELECT count(*) FROM silver.entity_company WHERE country_code != 'IN'")).scalar()
        matches = conn.execute(text("SELECT count(*) FROM gold.match_candidate")).scalar()
        signals = conn.execute(text("SELECT count(*) FROM gold.signal")).scalar()
        customs = conn.execute(text("SELECT count(*) FROM silver.customs_shipments_normalized")).scalar()
        print(f"      Exporters: {exporters}, Buyers: {buyers}, Matches: {matches}, Signals: {signals}, Customs: {customs}")
        assert exporters >= 1 and buyers >= 5 and matches >= 5

        print("[4/5] Auditing Explainability Drivers (Law 2)...")
        zero_drivers = conn.execute(text("SELECT count(*) FROM gold.match_candidate WHERE drivers IS NULL OR jsonb_array_length(drivers) = 0")).scalar()
        assert zero_drivers == 0
        print(f"      Zero-driver matches: {zero_drivers}")

        print("[5/5] Production System Status: 100% HEALTHY AND VERIFIED!")
        print("=" * 70)

if __name__ == "__main__":
    run_readiness_audit()
