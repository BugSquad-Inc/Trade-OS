import os
import sys
import uuid
from datetime import datetime, date, timezone
from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models.company import EntityCompany, EntityPerson, EntityProduct
from app.models.compliance import EntityCertification
from app.models.lane import TradeLaneBenchmark
from app.models.exporter import ExporterCapability
from app.models.signal import Signal, SignalEvidence
from app.models.match import MatchProfile, MatchCandidate, MatchScoreHistory
from app.models.provenance import SourceRegistry, EvidenceAssertion, TruthStatus, SourceTier
from app.models.product import ProductFamily, ProductVersion, ProductCertificate, ProductPassport
from app.services import scoring_service

def apply_sql_migrations():
    print("[1/3] Applying PostgreSQL Medallion DDL scripts & Provenance tables...")
    
    # Create gold.source_registry and gold.evidence_assertion if not exist
    ddl_provenance = """
    DO $$ BEGIN
        CREATE TYPE gold.source_tier_enum AS ENUM ('tier_a', 'tier_b', 'tier_c', 'tier_d', 'tier_e');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;

    DO $$ BEGIN
        CREATE TYPE gold.truth_status_enum AS ENUM ('verified', 'inferred', 'customer_supplied', 'provider_supplied', 'demo', 'stale', 'disputed', 'unavailable');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;

    CREATE TABLE IF NOT EXISTS gold.source_registry (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL UNIQUE,
        source_tier gold.source_tier_enum DEFAULT 'tier_e' NOT NULL,
        licence_terms TEXT,
        usage_policy VARCHAR(255),
        owner VARCHAR(100) DEFAULT 'Trade OS Data Operations',
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        checked_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
    );

    CREATE TABLE IF NOT EXISTS gold.evidence_assertion (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        claim_type VARCHAR(100) NOT NULL,
        claim_value JSONB NOT NULL,
        truth_status gold.truth_status_enum DEFAULT 'demo' NOT NULL,
        source_id UUID REFERENCES gold.source_registry(id) ON DELETE CASCADE,
        confidence FLOAT DEFAULT 1.0 NOT NULL,
        verification_method VARCHAR(255),
        reviewed_by VARCHAR(100),
        tenant_id UUID,
        metadata JSONB DEFAULT '{}'::jsonb,
        valid_from TIMESTAMPTZ DEFAULT NOW() NOT NULL,
        valid_until TIMESTAMPTZ,
        checked_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_evidence_claim_type ON gold.evidence_assertion (claim_type);
    CREATE INDEX IF NOT EXISTS idx_evidence_truth_status ON gold.evidence_assertion (truth_status);

    -- Silver Person Constraint Migration
    ALTER TABLE silver.entity_person DROP CONSTRAINT IF EXISTS entity_person_verification_status_check;
    ALTER TABLE silver.entity_person ADD CONSTRAINT entity_person_verification_status_check CHECK (verification_status IN ('unverified', 'pending', 'verified', 'bounced', 'demo'));

    -- Exporter Capability India Fields Migration
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS pan TEXT;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS gstin_list JSONB DEFAULT '["33AABCB1234F1Z1"]'::jsonb;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS iec TEXT DEFAULT '0498765432';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS udyam_number TEXT DEFAULT 'UDYAM-TN-02-0012345';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS rcmc_number TEXT DEFAULT 'CLE/SR/RCMC/2024/9876';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS rcmc_expiry DATE;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS lut_status TEXT DEFAULT 'active';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS lut_expiry DATE;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS ad_code TEXT DEFAULT '6390001';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS ad_bank_branch TEXT DEFAULT 'State Bank of India, Overseas Branch, Chennai';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS ad_bank_ifsc TEXT DEFAULT 'SBIN0000853';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS icegate_status TEXT DEFAULT 'registered';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS authorised_signatory TEXT DEFAULT 'K. S. Butler, Managing Director';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS facilities JSONB DEFAULT '[{"name": "Ambur Tannery Unit 1", "area_sqft": 45000, "workers": 85}]'::jsonb;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS ports JSONB DEFAULT '["INMAA", "INTUT"]'::jsonb;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS incoterms_preference JSONB DEFAULT '["FOB", "CIF", "DAP"]'::jsonb;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS commercial_constraints TEXT DEFAULT 'LC 60 days or 30% advance on custom tannages';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS onboarding_step INT DEFAULT 5;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS onboarding_status TEXT DEFAULT 'approved';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS reviewed_by TEXT DEFAULT 'Trade OS Senior Export Analyst';
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;
    ALTER TABLE gold.exporter_capability ADD COLUMN IF NOT EXISTS evidence_status JSONB DEFAULT '{"pan": "verified", "gstin": "verified", "iec": "verified", "ad_code": "verified", "rcmc": "verified", "lut": "verified"}'::jsonb;

    -- Product Domain Tables
    CREATE TABLE IF NOT EXISTS gold.product_family (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        tenant_id UUID,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(100) DEFAULT 'Finished Leather' NOT NULL,
        hs_code VARCHAR(20) DEFAULT '4107' NOT NULL,
        itc_hs_code VARCHAR(20) DEFAULT '4107.12.00',
        leather_type VARCHAR(100) DEFAULT 'Bovine Full Grain' NOT NULL,
        description TEXT,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
    );

    CREATE TABLE IF NOT EXISTS gold.product_version (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        product_family_id UUID REFERENCES gold.product_family(id) ON DELETE CASCADE NOT NULL,
        version_tag VARCHAR(50) DEFAULT 'v1.0' NOT NULL,
        materials JSONB DEFAULT '["Bovine Hide"]'::jsonb NOT NULL,
        finishes JSONB DEFAULT '["Semi-aniline"]'::jsonb NOT NULL,
        thickness_range_mm JSONB DEFAULT '["1.2-1.4"]'::jsonb NOT NULL,
        monthly_capacity_sqft INT DEFAULT 25000 NOT NULL,
        moq_sqft INT DEFAULT 2000 NOT NULL,
        lead_time_days INT DEFAULT 30 NOT NULL,
        sample_lead_time_days INT DEFAULT 7 NOT NULL,
        price_basis_inr FLOAT DEFAULT 280.0 NOT NULL,
        price_basis_usd FLOAT DEFAULT 3.35 NOT NULL,
        incoterms JSONB DEFAULT '["FOB Chennai", "CIF Hamburg"]'::jsonb NOT NULL,
        status VARCHAR(50) DEFAULT 'approved' NOT NULL,
        approved_by VARCHAR(100) DEFAULT 'Quality Lead',
        approved_at TIMESTAMPTZ,
        created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
    );

    CREATE TABLE IF NOT EXISTS gold.product_certificate (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        product_version_id UUID REFERENCES gold.product_version(id) ON DELETE CASCADE NOT NULL,
        cert_type VARCHAR(50) NOT NULL,
        certificate_name VARCHAR(255) NOT NULL,
        issuer VARCHAR(255) NOT NULL,
        accredited_lab VARCHAR(255) DEFAULT 'Eurofins / TÜV Rheinland',
        scope TEXT,
        file_hash VARCHAR(64),
        issue_date DATE NOT NULL,
        expiry_date DATE,
        status VARCHAR(50) DEFAULT 'verified' NOT NULL,
        verified_by VARCHAR(100) DEFAULT 'Trade OS Compliance Analyst',
        verified_at TIMESTAMPTZ DEFAULT NOW(),
        created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
    );

    CREATE TABLE IF NOT EXISTS gold.product_passport (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        product_version_id UUID REFERENCES gold.product_version(id) ON DELETE CASCADE NOT NULL,
        passport_number VARCHAR(100) UNIQUE NOT NULL,
        status VARCHAR(50) DEFAULT 'active' NOT NULL,
        recipient_buyer_id UUID,
        generated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
        metadata JSONB DEFAULT '{"eudr_clearance": "Grade A", "reach_compliant": true}'::jsonb NOT NULL
    );
    """
    
    with engine.connect() as conn:
        conn.execute(text(ddl_provenance))
        conn.commit()

    sql_dir = os.path.join(os.path.dirname(__file__), "..", "..", "sql")
    if os.path.exists(sql_dir):
        sql_files = sorted([f for f in os.listdir(sql_dir) if f.endswith(".sql")])
        with engine.connect() as conn:
            for fname in sql_files:
                fpath = os.path.join(sql_dir, fname)
                print(f"  -> Executing {fname}...")
                with open(fpath, "r", encoding="utf-8") as f:
                    sql_content = f.read()
                    conn.execute(text(sql_content))
                    conn.commit()
    print("  [OK] DDL migrations applied successfully.")

def seed_database():
    print("[2/3] Seeding Butler's Leather, 5 German Buyers, Provenance Source Registry...")
    db = SessionLocal()
    try:
        # 1. Seed Demo Source Registry
        demo_source = db.query(SourceRegistry).filter_by(name="TradeOS Synthetic Benchmark & Prototype Dataset (Demo)").first()
        if not demo_source:
            demo_source = SourceRegistry(
                id=uuid.uuid4(),
                name="TradeOS Synthetic Benchmark & Prototype Dataset (Demo)",
                source_tier=SourceTier.tier_e,
                licence_terms="Synthetic sample data for demonstration, workflow validation, and testing only.",
                usage_policy="Demo & Testing Environment Only",
                owner="Trade OS Founder & Research Sandbox",
                is_active=True,
                checked_at=datetime.now(timezone.utc)
            )
            db.add(demo_source)
            db.commit()
            db.refresh(demo_source)

        # Check if Products are already seeded
        prod_count = db.query(ProductFamily).count()
        if prod_count == 0:
            print("  [INFO] Seeding 3 Product Families & Passports for Butler's Leather...")
            
            # Product 1: Bovine Full-Grain Classic Nappa
            p1 = ProductFamily(
                id=uuid.uuid4(),
                name="Bovine Full-Grain Classic Nappa",
                category="Finished Bovine Leather",
                hs_code="4107",
                itc_hs_code="4107.12.00",
                leather_type="Full Grain Bovine",
                description="Premium bovine full grain leather with supple temper, aniline finish, crafted for luxury handbags and small leather goods."
            )
            db.add(p1)
            db.commit()
            db.refresh(p1)

            v1 = ProductVersion(
                product_family_id=p1.id,
                version_tag="v1.0",
                materials=["Bovine hide", "Vegetable-chrome synthetic combo"],
                finishes=["Semi-aniline", "Soft milled"],
                thickness_range_mm=["1.1-1.3", "1.3-1.5"],
                monthly_capacity_sqft=25000,
                moq_sqft=2000,
                lead_time_days=30,
                sample_lead_time_days=7,
                price_basis_inr=295.0,
                price_basis_usd=3.55,
                incoterms=["FOB Chennai", "CIF Hamburg"],
                status="approved",
                approved_by="Quality Director"
            )
            db.add(v1)
            db.commit()
            db.refresh(v1)

            c1 = ProductCertificate(
                product_version_id=v1.id,
                cert_type="LWG",
                certificate_name="LWG Gold Medal Environmental Audit",
                issuer="Leather Working Group",
                accredited_lab="BLC Leather Technology Centre",
                scope="Environmental management, water recycling, energy efficiency",
                issue_date=date(2025, 4, 1),
                expiry_date=date(2027, 4, 1),
                status="verified",
                verified_by="Trade OS Senior Compliance Auditor"
            )
            c2 = ProductCertificate(
                product_version_id=v1.id,
                cert_type="REACH_TEST",
                certificate_name="REACH SVHC 240+ Substances Zero-Detection Report",
                issuer="Eurofins India",
                accredited_lab="Eurofins Consumer Product Testing",
                scope="Chromium VI, Formaldehyde, Azo Dyes, Heavy Metals",
                issue_date=date(2026, 1, 15),
                expiry_date=date(2027, 1, 15),
                status="verified",
                verified_by="Trade OS Senior Compliance Auditor"
            )
            db.add_all([c1, c2])

            pass1 = ProductPassport(
                product_version_id=v1.id,
                passport_number="DPP-IN-BOV-4107-001",
                status="active",
                passport_metadata={
                    "origin": "Chennai / Ranipet Cluster, India",
                    "tannery_lwg_rating": "Gold",
                    "reach_tested": True,
                    "eudr_polygon_status": "DDS Ready",
                    "carbon_footprint_kg_co2_sqft": 1.42
                }
            )
            db.add(pass1)

            # Product 2: Finished Goat Nappa for Fine Gloves
            p2 = ProductFamily(
                id=uuid.uuid4(),
                name="Supple Goat Nappa for Gloves & Accessories",
                category="Finished Goat Leather",
                hs_code="4106",
                itc_hs_code="4106.21.00",
                leather_type="Goat Nappa",
                description="Ultra-soft kid/goat nappa with high tensile strength and colorfastness, tailored for gloves, wallets, and garment trim."
            )
            db.add(p2)
            db.commit()
            db.refresh(p2)

            v2 = ProductVersion(
                product_family_id=p2.id,
                version_tag="v1.0",
                materials=["Southern Indian Goat Skins", "Chrome-free Metal-free Tanning"],
                finishes=["Aniline", "Water-repellent"],
                thickness_range_mm=["0.5-0.7", "0.7-0.9"],
                monthly_capacity_sqft=15000,
                moq_sqft=1500,
                lead_time_days=25,
                sample_lead_time_days=5,
                price_basis_inr=240.0,
                price_basis_usd=2.90,
                incoterms=["FOB Chennai", "CIF Munich"],
                status="approved",
                approved_by="Quality Director"
            )
            db.add(v2)
            db.commit()
            db.refresh(v2)

            c3 = ProductCertificate(
                product_version_id=v2.id,
                cert_type="CHROMIUM_VI",
                certificate_name="ISO 17075-1:2017 Chromium VI Non-Detectable Test",
                issuer="TÜV SÜD South Asia",
                accredited_lab="TÜV SÜD Leather Lab",
                scope="Chromium VI determination after aging test (<3 mg/kg DL)",
                issue_date=date(2026, 2, 10),
                expiry_date=date(2027, 2, 10),
                status="verified",
                verified_by="Trade OS Senior Compliance Auditor"
            )
            db.add(c3)

            pass2 = ProductPassport(
                product_version_id=v2.id,
                passport_number="DPP-IN-GOAT-4106-002",
                status="active",
                passport_metadata={
                    "origin": "Ambur Cluster, Tamil Nadu, India",
                    "chromium_vi_free": True,
                    "metal_free_tannage": True,
                    "reach_tested": True
                }
            )
            db.add(pass2)

            # Product 3: Heavy Vegetable Tanned Bridle & Saddlery Cowhide
            p3 = ProductFamily(
                id=uuid.uuid4(),
                name="Heavy Vegetable Tanned Bridle & Saddle Cowhide",
                category="Vegetable Tanned Leather",
                hs_code="4107",
                itc_hs_code="4107.92.00",
                leather_type="Heavy Cowhide",
                description="Traditional pit-tanned heavy cowhide infused with natural waxes and tallows for equestrian saddles and harnesses."
            )
            db.add(p3)
            db.commit()
            db.refresh(p3)

            v3 = ProductVersion(
                product_family_id=p3.id,
                version_tag="v1.0",
                materials=["Heavy Bovine Hide", "Mimosa & Chestnut Bark Extracts"],
                finishes=["Hot-stuffed wax finish", "Glazed edge"],
                thickness_range_mm=["1.8-2.2", "2.2-2.8"],
                monthly_capacity_sqft=10000,
                moq_sqft=1000,
                lead_time_days=40,
                sample_lead_time_days=10,
                price_basis_inr=350.0,
                price_basis_usd=4.20,
                incoterms=["FOB Chennai", "CIF Hamburg"],
                status="approved",
                approved_by="Master Tanner"
            )
            db.add(v3)
            db.commit()
            db.refresh(v3)

            c4 = ProductCertificate(
                product_version_id=v3.id,
                cert_type="ISO14001",
                certificate_name="ISO 14001:2015 Environmental Management Standard",
                issuer="DQS India",
                accredited_lab="DQS Certification",
                scope="100% Bio-based vegetable tanning extracts verification",
                issue_date=date(2025, 6, 1),
                expiry_date=date(2028, 6, 1),
                status="verified",
                verified_by="Trade OS Senior Compliance Auditor"
            )
            db.add(c4)

            pass3 = ProductPassport(
                product_version_id=v3.id,
                passport_number="DPP-IN-VEG-4107-003",
                status="active",
                passport_metadata={
                    "origin": "Ranipet Traditional Tannery Park, India",
                    "100_percent_veg_tanned": True,
                    "biodegradable": True,
                    "zero_synthetic_polymers": True
                }
            )
            db.add(pass3)
            db.commit()
            print("  [OK] Successfully seeded 3 Product Passports with lab certificates.")
            # 2. Seed Butler's Leather Exporter Capability
            exporter = ExporterCapability(
                id=uuid.uuid4(),
                company_name="Butler's Leather",
                location="Chennai, Tamil Nadu, India",
                cluster="Chennai / Ambur / Ranipet Leather Cluster",
                export_market_focus=["Germany", "EU", "United Kingdom"],
                material_types=["Finished bovine full-grain", "Finished goat nappa", "Vegetable crust", "Footwear uppers", "Lining leather"],
                tannage=["Vegetable-tanned", "Chrome-tanned", "Chrome-free / Metal-free", "Combination"],
                thickness_range_mm=["0.8-1.0", "1.2-1.4", "1.6-2.2"],
                finish_capabilities=["Aniline", "Semi-aniline", "Pigmented", "Pull-up", "Wax finish", "Embossed print"],
                monthly_capacity_sqft=50000,
                moq_sqft=3000,
                lead_time_days=35,
                sample_lead_time_days=10,
                port_of_export="Chennai Port (INMAA)",
                incoterms=["FOB Chennai", "CIF Hamburg", "EXW"],
                certifications=["LWG Gold Rated", "ISO 9001:2015", "ISO 14001:2015", "REACH SVHC Tested"],
                eudr_readiness_score=68,
                eudr_gap_summary="Missing farm-level GPS polygon coordinates for ~30% smallholder hide supply cluster; Due Diligence Statement (DDS) template ready."
            )
            db.add(exporter)

            # 3. Seed Freight Lane Benchmark
            lane = TradeLaneBenchmark(
                id=uuid.uuid4(),
                origin_country="IN",
                origin_port="INMAA",
                destination_country="DE",
                destination_port="DEHAM",
                mode="sea",
                container_type="40HC",
                rate_usd=1850.0,
                rate_low_usd=1800.0,
                rate_high_usd=2600.0,
                transit_days_min=26,
                transit_days_max=34,
                port_congestion_index="Normal (1.2 days wait)",
                reroute_risk_notes="Suez canal security advisories may require Cape of Good Hope routing (+10-14 days)",
                effective_start=date(2026, 1, 1)
            )
            db.add(lane)

            # 4. Seed 5 German Buyers (Fictionalized sample dossiers with demo markers)
            buyers_data = [
                {
                    "name": "Picard GmbH [Sample]",
                    "legal_name": "Picard Lederwaren GmbH & Co. KG",
                    "city": "Obertshausen",
                    "region": "Hesse",
                    "domain": "picard-lederwaren.de",
                    "website": "https://www.picard-lederwaren.de",
                    "linkedin_url": "https://www.linkedin.com/company/picard-lederwaren",
                    "segment": "Premium Leather Goods & Bags",
                    "description": "Renowned German heritage leather goods manufacturer producing premium handbags, wallets, and travel accessories requiring fine calf/bovine leather.",
                    "founded_year": 1928,
                    "employee_range": "200-500",
                    "contact": {
                        "name": "Johann Schmidt (Sample Contact)",
                        "title": "Head of Sourcing & Leather Procurement",
                        "email": "j.schmidt@picard-leather-demo.de",
                        "phone": "+49 6104 7040",
                        "confidence": 0.88,
                        "verification_status": "demo"
                    },
                    "products": [
                        {"name": "Full-Grain Bovine Leather for Handbags", "hs_code": "4107", "material_types": ["Full-grain calf", "Bovine leather"], "thickness": ["0.9-1.3"], "finish": ["Semi-aniline", "Pigmented"]}
                    ],
                    "certifications": [
                        {"type": "REACH", "name": "REACH SVHC Test Declaration", "issued_by": "TUV Rheinland"},
                        {"type": "LWG", "name": "LWG Leather Sourcing Mandate", "issued_by": "Leather Working Group"}
                    ],
                    "signals": [
                        {
                            "category": "compliance",
                            "severity": "high",
                            "title": "Market Chemical & Traceability Update for Leather Goods",
                            "summary": "Picard sustainability update highlights mandatory batch-level declarations for all imported leathers.",
                            "quote": "We are requiring all non-EU tanneries to provide farm geolocation data and REACH chemical compliance certificates prior to 2026 collection orders.",
                            "score": 90
                        },
                        {
                            "category": "intent",
                            "severity": "medium",
                            "title": "Expansion of Sustainable Leather Bag Collection",
                            "summary": "Picard announced new sustainable accessory line requiring LWG Gold certified leather supply partners.",
                            "quote": "Expanding premium leather accessory range with emphasis on certified ethical tanneries in South Asia.",
                            "score": 85
                        }
                    ]
                },
                {
                    "name": "Roeckl Handschuhe & Accessoires [Sample]",
                    "legal_name": "Roeckl Handschuhe & Accessoires GmbH & Co. KG",
                    "city": "Munich",
                    "region": "Bavaria",
                    "domain": "roeckl.com",
                    "website": "https://www.roeckl.com",
                    "linkedin_url": "https://www.linkedin.com/company/roeckl",
                    "segment": "Luxury Gloves & Fine Accessories",
                    "description": "Munich-based purveyor of royal warrant glovemaking, specialized in ultra-soft kid/goat nappa, equestrian riding gloves, and fine silk-lined accessories.",
                    "founded_year": 1839,
                    "employee_range": "100-250",
                    "contact": {
                        "name": "Klaus Weber (Sample Contact)",
                        "title": "Sourcing Director Glove Materials",
                        "email": "k.weber@roeckl-gloves-demo.de",
                        "phone": "+49 89 72080",
                        "confidence": 0.85,
                        "verification_status": "demo"
                    },
                    "products": [
                        {"name": "Ultra-Soft Goat & Kid Nappa", "hs_code": "4106", "material_types": ["Kid nappa", "Goat nappa"], "thickness": ["0.5-0.8"], "finish": ["Aniline", "Water-repellent"]}
                    ],
                    "certifications": [
                        {"type": "REACH", "name": "REACH Chromium VI Testing", "issued_by": "Eurofins"}
                    ],
                    "signals": [
                        {
                            "category": "intent",
                            "severity": "high",
                            "title": "Winter Equestrian & Glove Collection Sourcing Push",
                            "summary": "Procurement team expanding search for high-tensile goat nappa with high colorfastness for seasonal lines.",
                            "quote": "Sourcing supple kidskins and goat leathers meeting rigorous dry/wet rub tests for luxury glove production.",
                            "score": 88
                        }
                    ]
                },
                {
                    "name": "Bader GmbH & Co. KG [Sample]",
                    "legal_name": "Bader GmbH & Co. KG",
                    "city": "Göppingen",
                    "region": "Baden-Württemberg",
                    "domain": "bader-leather.com",
                    "website": "https://www.bader-leather.com",
                    "linkedin_url": "https://www.linkedin.com/company/bader-leather",
                    "segment": "Automotive Interior Leather",
                    "description": "One of the world's leading automotive leather suppliers for premium OEM vehicles (Mercedes-Benz, BMW, Porsche, Audi) demanding strict defect-free bovine hides.",
                    "founded_year": 1872,
                    "employee_range": "1000+",
                    "contact": {
                        "name": "Marcus Becker (Sample Contact)",
                        "title": "Supplier Quality & Raw Material Procurement",
                        "email": "m.becker@bader-leather-demo.de",
                        "phone": "+49 7161 6720",
                        "confidence": 0.82,
                        "verification_status": "demo"
                    },
                    "products": [
                        {"name": "Bovine Wet-Blue & Crust for Auto Upholstery", "hs_code": "4104", "material_types": ["Bovine crust", "Heavy hide"], "thickness": ["1.2-1.8"], "finish": ["Crust", "Semi-aniline"]}
                    ],
                    "certifications": [
                        {"type": "IATF", "name": "IATF 16949 / ISO 9001", "issued_by": "DQS"},
                        {"type": "REACH", "name": "Automotive Raw Hide Traceability Protocol", "issued_by": "VDA"}
                    ],
                    "signals": [
                        {
                            "category": "regulatory",
                            "severity": "critical",
                            "title": "Automotive Supply Chain LkSG & Quality Audit",
                            "summary": "Bader supplier quality team enforces strict origin tracing for all imported wet-blue and crust containers.",
                            "quote": "All Tier-2 tanneries must document raw material origin and demonstrate zero chemical defect compliance.",
                            "score": 92
                        }
                    ]
                },
                {
                    "name": "Kilger [Sample]",
                    "legal_name": "Gerberei Kilger GmbH",
                    "city": "Viechtach",
                    "region": "Bavaria",
                    "domain": "gerberei-kilger.de",
                    "website": "https://www.gerberei-kilger.de",
                    "linkedin_url": "https://www.linkedin.com/company/gerberei-kilger",
                    "segment": "Wholesale Leather Distributor",
                    "description": "Traditional Bavarian tannery and wholesale merchant distributing vegetable-tanned leathers, sole leathers, and footwear crust across Central Europe.",
                    "founded_year": 1856,
                    "employee_range": "50-100",
                    "contact": {
                        "name": "Stefan Kilger (Sample Contact)",
                        "title": "Managing Director & Sourcing Lead",
                        "email": "s.kilger@kilger-leder-demo.de",
                        "phone": "+49 9942 9440",
                        "confidence": 0.80,
                        "verification_status": "demo"
                    },
                    "products": [
                        {"name": "Vegetable Tanned Bovine Crust", "hs_code": "4104", "material_types": ["Veg-tan crust", "Sole leather"], "thickness": ["1.4-2.0"], "finish": ["Natural crust", "Oiled"]}
                    ],
                    "certifications": [
                        {"type": "LWG", "name": "LWG Environmental Audit", "issued_by": "LWG"}
                    ],
                    "signals": [
                        {
                            "category": "market",
                            "severity": "medium",
                            "title": "Wholesale Inventory Replenishment Run",
                            "summary": "Kilger wholesale catalogue shows steady demand for imported crust to buffer rising European raw hide costs.",
                            "quote": "Seeking consistent vegetable-tanned bovine crust in container quantities for footwear replenishment.",
                            "score": 78
                        }
                    ]
                },
                {
                    "name": "Otto Schumacher [Sample]",
                    "legal_name": "Otto Schumacher Sattlerei GmbH",
                    "city": "Dorsten",
                    "region": "North Rhine-Westphalia",
                    "domain": "otto-schumacher-sattlerei.de",
                    "website": "https://www.os-sattlerei.de",
                    "linkedin_url": "https://www.linkedin.com/company/otto-schumacher",
                    "segment": "Equestrian Saddlery & Harnesses",
                    "description": "High-end bespoke German saddlery crafting handcrafted dressage saddles, double bridles, and leather equestrian tack from heavy bovine leather.",
                    "founded_year": 1953,
                    "employee_range": "20-50",
                    "contact": {
                        "name": "Christian Schumacher (Sample Contact)",
                        "title": "Master Saddler & Material Procurement",
                        "email": "c.schumacher@schumacher-saddlery-demo.de",
                        "phone": "+49 2362 9900",
                        "confidence": 0.78,
                        "verification_status": "demo"
                    },
                    "products": [
                        {"name": "Heavy Bridle & Saddle Cowhide", "hs_code": "4107", "material_types": ["Heavy cowhide", "Bridle leather"], "thickness": ["1.8-2.4"], "finish": ["Waxed", "Vegetable-tanned"]}
                    ],
                    "certifications": [
                        {"type": "REACH", "name": "REACH Chemical Compliance", "issued_by": "DEKRA"}
                    ],
                    "signals": [
                        {
                            "category": "intent",
                            "severity": "medium",
                            "title": "Bespoke Equestrian Leather Tack Sourcing",
                            "summary": "Schumacher reviewing premium vegetable-tanned cowhide suppliers with high tensile strength for European export market.",
                            "quote": "Demanding heavy vegetable-tanned cowhide with defect-free grain and firm temper for custom saddle lines.",
                            "score": 75
                        }
                    ]
                }
            ]

            match_profile = MatchProfile(
                id=uuid.uuid4(),
                name="Butler's Leather Germany Expansion Profile",
                exporter_capability_id=exporter.id,
                objective="find_buyers",
                criteria={"target_countries": ["DE"], "target_segments": ["Leather goods", "Gloves", "Auto", "Saddlery"]}
            )
            db.add(match_profile)
            db.commit()

            for idx, b_data in enumerate(buyers_data, start=1):
                company = EntityCompany(
                    id=uuid.uuid4(),
                    canonical_name=b_data["name"],
                    legal_name=b_data["legal_name"],
                    country_code="DE",
                    city=b_data["city"],
                    region=b_data["region"],
                    domain=b_data["domain"],
                    website=b_data["website"],
                    linkedin_url=b_data["linkedin_url"],
                    segment=b_data["segment"],
                    description=b_data["description"],
                    founded_year=b_data["founded_year"],
                    employee_range=b_data["employee_range"],
                    status="active",
                    confidence=0.95
                )
                db.add(company)
                db.commit()
                db.refresh(company)

                # Add Contact with demo status
                contact_info = b_data["contact"]
                person = EntityPerson(
                    id=uuid.uuid4(),
                    company_id=company.id,
                    full_name=contact_info["name"],
                    title=contact_info["title"],
                    email=contact_info["email"],
                    phone=contact_info["phone"],
                    is_primary=True,
                    confidence=contact_info["confidence"],
                    verification_status=contact_info["verification_status"],
                    consent_status="legitimate_interest",
                    legal_basis="B2B legitimate interest under GDPR Art. 6(1)(f) (Demo Sample)"
                )
                db.add(person)

                # Add Products
                for p_info in b_data.get("products", []):
                    prod = EntityProduct(
                        id=uuid.uuid4(),
                        company_id=company.id,
                        name=p_info["name"],
                        hs_code=p_info.get("hs_code"),
                        material_types=p_info.get("material_types", []),
                        thickness_range_mm=p_info.get("thickness", []),
                        finish=p_info.get("finish", [])
                    )
                    db.add(prod)

                # Add Certifications
                for c_info in b_data.get("certifications", []):
                    cert = EntityCertification(
                        id=uuid.uuid4(),
                        company_id=company.id,
                        certification_type=c_info["type"],
                        certification_name=c_info["name"],
                        issued_by=c_info.get("issued_by"),
                        status="active"
                    )
                    db.add(cert)

                # Add Signals with Evidence Assertion
                for s_info in b_data.get("signals", []):
                    sig = Signal(
                        id=uuid.uuid4(),
                        entity_id=company.id,
                        category=s_info["category"],
                        severity=s_info["severity"],
                        title=s_info["title"],
                        summary=s_info["summary"],
                        quote=s_info.get("quote"),
                        score=s_info["score"],
                        evidence={"source": "Public Company Sustainability / Procurement Portal (Demo)", "quote": s_info.get("quote")}
                    )
                    db.add(sig)

                    # Also add to gold.evidence_assertion
                    evidence_assertion = EvidenceAssertion(
                        id=uuid.uuid4(),
                        claim_type="buyer_signal",
                        claim_value={"title": s_info["title"], "summary": s_info["summary"], "score": s_info["score"]},
                        truth_status=TruthStatus.demo,
                        source_id=demo_source.id,
                        confidence=0.9,
                        verification_method="Sample research dossier",
                        reviewed_by="Trade OS Analyst"
                    )
                    db.add(evidence_assertion)

                # Compute and store 100-Point Match Score
                match_score = scoring_service.score_match(company, exporter, rank=idx)
                
                candidate = MatchCandidate(
                    id=uuid.uuid4(),
                    match_profile_id=match_profile.id,
                    buyer_id=company.id,
                    total_score=match_score.total_score,
                    product_fit_score=match_score.product_fit_score,
                    compliance_score=match_score.compliance_score,
                    lane_economics_score=match_score.lane_economics_score,
                    intent_signals_score=match_score.intent_signals_score,
                    accessibility_score=match_score.accessibility_score,
                    grade=match_score.grade,
                    rank=idx,
                    score_version="v1.0.0",
                    drivers=[d.model_dump() for d in match_score.drivers],
                    key_gaps=match_score.key_gaps,
                    next_best_action=match_score.next_best_action,
                    outreach_angle=match_score.outreach_angle,
                    status="suggested"
                )
                db.add(candidate)

                # History: INSERT ONLY
                history = MatchScoreHistory(
                    buyer_id=company.id,
                    score=match_score.total_score,
                    score_version="v1.0.0",
                    drivers=[d.model_dump() for d in match_score.drivers]
                )
                db.add(history)
                db.commit()

        print("  [OK] Seed complete: Butler's Leather + 5 German Buyers + Provenance Source Registry created.")

    except Exception as e:
        db.rollback()
        print(f"  [ERROR] Seeding failed: {str(e)}")
        raise e
    finally:
        db.close()

def verify_seeding():
    print("[3/3] Verifying Database Seeding & Provenance...")
    db = SessionLocal()
    try:
        buyers_count = db.query(EntityCompany).filter(EntityCompany.country_code != "IN").count()
        exporter_count = db.query(ExporterCapability).count()
        matches_count = db.query(MatchCandidate).count()
        history_count = db.query(MatchScoreHistory).count()
        signals_count = db.query(Signal).count()
        lane_count = db.query(TradeLaneBenchmark).count()
        contacts_count = db.query(EntityPerson).count()
        sources_count = db.query(SourceRegistry).count()
        evidence_count = db.query(EvidenceAssertion).count()

        products_count = db.query(ProductFamily).count()
        passports_count = db.query(ProductPassport).count()

        print(f"  -> Exporter Profiles:   {exporter_count} (Expected >= 1)")
        print(f"  -> German Buyers:       {buyers_count} (Expected >= 5)")
        print(f"  -> Match Candidates:    {matches_count} (Expected >= 5)")
        print(f"  -> Score History:       {history_count} (Expected >= 5)")
        print(f"  -> Trade Signals:       {signals_count} (Expected 7+)")
        print(f"  -> Freight Lanes:       {lane_count} (Expected >= 1)")
        print(f"  -> Sample Contacts:     {contacts_count} (Expected 5+)")
        print(f"  -> Source Registries:   {sources_count} (Expected >= 1)")
        print(f"  -> Evidence Assertions: {evidence_count} (Expected >= 5)")
        print(f"  -> Product Families:    {products_count} (Expected >= 3)")
        print(f"  -> Digital Passports:   {passports_count} (Expected >= 3)")

        assert exporter_count >= 1, "Missing exporter profile"
        assert buyers_count >= 5, f"Expected at least 5 buyers, found {buyers_count}"
        assert matches_count >= 5, f"Expected at least 5 matches, found {matches_count}"
        assert history_count >= 5, "Missing score history"
        assert sources_count >= 1, "Missing source registry"
        assert evidence_count >= 5, "Missing evidence assertions"
        assert products_count >= 3, f"Expected at least 3 product families, found {products_count}"
        assert passports_count >= 3, f"Expected at least 3 digital passports, found {passports_count}"
        print("[SUCCESS] All seed, provenance, and product passport validation checks passed 100%!")
    finally:
        db.close()

if __name__ == "__main__":
    apply_sql_migrations()
    seed_database()
    verify_seeding()
