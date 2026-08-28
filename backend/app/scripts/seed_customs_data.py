from datetime import date, timedelta
from app.database import SessionLocal
from app.services.customs_service import CustomsIntelligenceService

SAMPLE_BOL_RECORDS = [
    {
        "bol_number": "MEDUIN9082341",
        "shipment_date": (date.today() - timedelta(days=5)).isoformat(),
        "importer_raw_name": "Picard GmbH",
        "exporter_raw_name": "Butler's Leather Tannery Chennai",
        "origin_country": "IN",
        "origin_port": "INMAA",
        "destination_country": "DE",
        "destination_port": "DEHAM",
        "hs_code": "410712",
        "product_desc": "Bovine grain split crust leather for luxury travel bags",
        "weight_kg": 7200.0,
        "teu_count": 1.0,
        "declared_value_usd": 68000.0
    },
    {
        "bol_number": "HLCUIN1029384",
        "shipment_date": (date.today() - timedelta(days=12)).isoformat(),
        "importer_raw_name": "Bader GmbH & Co. KG",
        "exporter_raw_name": "South India Tannery Corp",
        "origin_country": "IN",
        "origin_port": "INMAA",
        "destination_country": "DE",
        "destination_port": "DEHAM",
        "hs_code": "410792",
        "product_desc": "Automotive upholstery full-grain crust leather",
        "weight_kg": 14500.0,
        "teu_count": 2.0,
        "declared_value_usd": 132000.0
    },
    {
        "bol_number": "MSCUIN8837192",
        "shipment_date": (date.today() - timedelta(days=18)).isoformat(),
        "importer_raw_name": "Roeckl Handschuhe",
        "exporter_raw_name": "Ranipet Leather Finishing Works",
        "origin_country": "IN",
        "origin_port": "INMAA",
        "destination_country": "DE",
        "destination_port": "DEHAM",
        "hs_code": "410621",
        "product_desc": "Finished goat nappa leather for luxury dress gloves",
        "weight_kg": 3800.0,
        "teu_count": 1.0,
        "declared_value_usd": 49000.0
    },
    {
        "bol_number": "CMAUIN4928173",
        "shipment_date": (date.today() - timedelta(days=25)).isoformat(),
        "importer_raw_name": "Gucci S.p.A.",
        "exporter_raw_name": "Chennai Premium Calfskin Ltd",
        "origin_country": "IN",
        "origin_port": "INMAA",
        "destination_country": "IT",
        "destination_port": "ITGOA",
        "hs_code": "410711",
        "product_desc": "Full-grain calf nappa leather for Italian maroquinerie",
        "weight_kg": 8900.0,
        "teu_count": 1.0,
        "declared_value_usd": 94000.0
    },
    {
        "bol_number": "HAPAGIN7728190",
        "shipment_date": (date.today() - timedelta(days=31)).isoformat(),
        "importer_raw_name": "Hermès International",
        "exporter_raw_name": "Ambur Veg-Tanned Heritage Tannery",
        "origin_country": "IN",
        "origin_port": "INMAA",
        "destination_country": "FR",
        "destination_port": "FRLEH",
        "hs_code": "410411",
        "product_desc": "Vegetable tanned bovine saddle leather hides",
        "weight_kg": 6400.0,
        "teu_count": 1.0,
        "declared_value_usd": 86000.0
    }
]

def seed_customs():
    print("[CUSTOMS BOL SEED] Ingesting Bill of Lading Manifest Records...")
    db = SessionLocal()
    try:
        res = CustomsIntelligenceService.ingest_bol_records(db, SAMPLE_BOL_RECORDS)
        print(f"[SUCCESS] Ingested {res['ingested_count']} BOL shipments and emitted {res['signals_emitted']} trade signals.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_customs()
