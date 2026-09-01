#!/usr/bin/env python3
"""
Trade OS — Inspect and Export PostgreSQL Database Content
Extracts table inventories, row counts, and sample records from Docker PostgreSQL container.
"""

import json
from datetime import datetime, timezone, date
from uuid import UUID
from decimal import Decimal
from pathlib import Path
from sqlalchemy import create_engine, text

DB_URL = "postgresql+psycopg://tradeos:tradeos_secret_password@localhost:5433/trade_os"
OUTPUT_DIR = Path(__file__).resolve().parent / "db_exports"
OUTPUT_DIR.mkdir(exist_ok=True)

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

def main():
    engine = create_engine(DB_URL)
    snapshot = {"extracted_at": datetime.now(timezone.utc).isoformat(), "tables": {}, "sample_data": {}}

    print("=" * 70)
    print("       [Trade OS] POSTGRESQL DATABASE CONTENT AUDIT")
    print("=" * 70)

    with engine.connect() as conn:
        # 1. Schemas
        schemas_res = conn.execute(text(
            "SELECT schema_name FROM information_schema.schemata "
            "WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast') "
            "ORDER BY schema_name;"
        )).fetchall()
        schemas = [r[0] for r in schemas_res]
        print(f"Active Schemas ({len(schemas)}): {', '.join(schemas)}\n")

        # 2. Tables & Row Counts
        tables_res = conn.execute(text(
            "SELECT table_schema, table_name FROM information_schema.tables "
            "WHERE table_schema NOT IN ('pg_catalog', 'information_schema') "
            "ORDER BY table_schema, table_name;"
        )).fetchall()

        print(f"Total Tables: {len(tables_res)}\n")
        print(f"{'Schema.Table':<45} | {'Row Count':>10}")
        print("-" * 60)

        for schema, table in tables_res:
            full_name = f"{schema}.{table}"
            try:
                count = conn.execute(text(f'SELECT count(*) FROM "{schema}"."{table}"')).scalar()
                snapshot["tables"][full_name] = count
                print(f"{full_name:<45} | {count:>10}")
            except Exception as e:
                snapshot["tables"][full_name] = f"Error: {e}"
                print(f"{full_name:<45} | {'ERROR':>10}")

        print("\n" + "=" * 70)
        print("       KEY TABLE SAMPLE DATA SUMMARY")
        print("=" * 70)

        key_tables = [
            ("silver", "entity_company", "Buyers & Suppliers"),
            ("silver", "entity_product", "Cataloged Products"),
            ("silver", "trade_lane_benchmark", "Freight Lanes"),
            ("gold", "exporter_capability", "Butler's Leather Profile"),
            ("gold", "match_candidate", "Top Matches & Scores"),
            ("gold", "signal", "Live Signals"),
            ("gold", "product_family", "Product Families & DPP"),
            ("gold", "opportunity", "Deal Pipeline Opportunities"),
            ("gold", "tenant", "Multi-Tenant Orgs"),
            ("gold", "user_account", "User Accounts")
        ]

        for schema, table, label in key_tables:
            full_name = f"{schema}.{table}"
            if full_name not in snapshot["tables"]:
                continue
            
            try:
                rows = conn.execute(text(f'SELECT * FROM "{schema}"."{table}" LIMIT 5')).mappings().all()
                data = [dict(r) for r in rows]
                snapshot["sample_data"][full_name] = data
                print(f"\n[*] {label} ({full_name} — showing up to 5 rows):")
                if not data:
                    print("   [Empty Table]")
                else:
                    for idx, row in enumerate(data, 1):
                        summary = {k: v for k, v in row.items() if k in ('id', 'name', 'legal_name', 'score', 'status', 'title', 'trade_lane', 'origin_port', 'destination_port', 'email', 'country')}
                        if not summary:
                            summary = {k: row[k] for k in list(row.keys())[:4]}
                        print(f"   Row {idx}: {summary}")
            except Exception as e:
                print(f"   Could not fetch sample for {full_name}: {e}")

    # Write snapshot JSON
    out_file = OUTPUT_DIR / "db_snapshot.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, cls=CustomEncoder)
    print(f"\n[OK] Full structured snapshot exported to: {out_file}")

if __name__ == "__main__":
    main()
