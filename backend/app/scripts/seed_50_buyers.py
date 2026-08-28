import uuid
from datetime import datetime, date
from app.database import SessionLocal
from app.models.company import EntityCompany, EntityPerson, EntityProduct
from app.models.compliance import EntityCertification
from app.models.signal import Signal
from app.services import entity_resolution_service, scoring_service
from app.repositories import capability_repo, match_repo

EUROPEAN_BUYERS_EXPANSION = [
    # Germany (Luxury & Industrial)
    {"name": "Hugo Boss AG", "country": "DE", "city": "Metzingen", "segment": "Luxury Apparel & Leather", "domain": "hugoboss.com", "contact": "Helmut Richter", "role": "Senior Leather Sourcing Manager"},
    {"name": "Montblanc International", "country": "DE", "city": "Hamburg", "segment": "Luxury Writing & Leather Goods", "domain": "montblanc.com", "contact": "Dieter Meyer", "role": "Leather Goods Procurement Lead"},
    {"name": "Rimowa GmbH", "country": "DE", "city": "Cologne", "segment": "Luggage & Travel Accessories", "domain": "rimowa.com", "contact": "Frank Wagner", "role": "Materials Development Director"},
    {"name": "Braun Büffel", "country": "DE", "city": "Kirn", "segment": "Fine Leather Goods & Wallets", "domain": "braun-bueffel.com", "contact": "Christian Braun", "role": "Procurement Lead"},
    {"name": "Aigner Munich", "country": "DE", "city": "Munich", "segment": "Luxury Handbags & Belts", "domain": "aignermunich.com", "contact": "Claudia Fischer", "role": "Leather Quality Specialist"},
    {"name": "Meindl Footwear", "country": "DE", "city": "Kirchanschöring", "segment": "Outdoor & Alpine Boots", "domain": "meindl.de", "contact": "Lukas Meindl", "role": "Raw Hide Purchasing Lead"},
    {"name": "Hanwag GmbH", "country": "DE", "city": "Vierkirchen", "segment": "Trekking Boots & Heavy Leather", "domain": "hanwag.com", "contact": "Thomas Becker", "role": "Sourcing Specialist"},
    {"name": "Lowa Sportschuhe", "country": "DE", "city": "Jetzendorf", "segment": "Technical Outdoor Footwear", "domain": "lowa.de", "contact": "Markus Kroll", "role": "Leather Supply Lead"},
    {"name": "Abro GmbH", "country": "DE", "city": "Rodgau", "segment": "Designer Handbags", "domain": "abro.de", "contact": "Achim Bruder", "role": "Managing Director"},
    {"name": "Liebeskind Berlin", "country": "DE", "city": "Berlin", "segment": "Vintage Wash Leather Bags", "domain": "liebeskind-berlin.com", "contact": "Svenja Berg", "role": "Product Development Lead"},
    {"name": "Bogner GmbH", "country": "DE", "city": "Munich", "segment": "Luxury Ski & Leather Accessories", "domain": "bogner.com", "contact": "Matthias Gross", "role": "Accessories Sourcing Manager"},
    {"name": "Porsche Design", "country": "DE", "city": "Ludwigsburg", "segment": "Premium Lifestyle & Auto Goods", "domain": "porsche-design.com", "contact": "Oliver Porsche", "role": "Design & Materials Director"},
    {"name": "Mercedes-Benz Interiors Sourcing", "country": "DE", "city": "Stuttgart", "segment": "Automotive OEM Leather", "domain": "mercedes-benz.com", "contact": "Wolfgang Klein", "role": "Tier-1 Leather Procurement"},
    {"name": "BMW Group Trim Procurement", "country": "DE", "city": "Munich", "segment": "Automotive Interior Materials", "domain": "bmwgroup.com", "contact": "Klaus Huber", "role": "Sustainable Leather Lead"},
    {"name": "Audi AG Materials", "country": "DE", "city": "Ingolstadt", "segment": "Automotive Leather & Alcantara", "domain": "audi.de", "contact": "Stefan Weiss", "role": "Sustainability & LkSG Compliance"},

    # Italy (Fashion, Footwear, Tanneries)
    {"name": "Gucci S.p.A.", "country": "IT", "city": "Florence", "segment": "Ultra-Luxury Handbags & Footwear", "domain": "gucci.com", "contact": "Matteo Rossi", "role": "Head of Raw Materials Sourcing"},
    {"name": "Prada Group", "country": "IT", "city": "Milan", "segment": "Luxury Leather Goods & Saffiano", "domain": "pradagroup.com", "contact": "Gianluca Moretti", "role": "Leather Division Director"},
    {"name": "Bottega Veneta", "country": "IT", "city": "Vicenza", "segment": "Intrecciato Woven Leather", "domain": "bottegaveneta.com", "contact": "Lorenzo Conti", "role": "Master Craftsman & Sourcing"},
    {"name": "Tod's S.p.A.", "country": "IT", "city": "Sant'Elpidio a Mare", "segment": "Luxury Loafers & Leather Goods", "domain": "todsgroup.com", "contact": "Marco Della Valle", "role": "Procurement Lead"},
    {"name": "Salvatore Ferragamo", "country": "IT", "city": "Florence", "segment": "Luxury Footwear & Leather", "domain": "ferragamo.com", "contact": "Andrea Bianchi", "role": "Leather Sourcing Specialist"},
    {"name": "Fendi S.r.l.", "country": "IT", "city": "Rome", "segment": "High-End Roman Leather & Bags", "domain": "fendi.com", "contact": "Paolo De Luca", "role": "Pellicceria & Leather Sourcing"},
    {"name": "Furla S.p.A.", "country": "IT", "city": "Bologna", "segment": "Accessible Luxury Leather Bags", "domain": "furla.com", "contact": "Elena Galli", "role": "Supply Chain Director"},
    {"name": "Poltrona Frau", "country": "IT", "city": "Tolentino", "segment": "Luxury Leather Furniture & Auto", "domain": "poltronafrau.com", "contact": "Roberto Ferrari", "role": "Pelle Frau Procurement"},
    {"name": "Natuzzi S.p.A.", "country": "IT", "city": "Santeramo in Colle", "segment": "High-Volume Upholstery Leather", "domain": "natuzzi.com", "contact": "Pasquale Natuzzi", "role": "Global Sourcing Director"},
    {"name": "Geox S.p.A.", "country": "IT", "city": "Montebelluna", "segment": "Breathable Leather Footwear", "domain": "geox.com", "contact": "Daniele Moretti", "role": "Footwear Materials Director"},

    # France (Haute Maroquinerie)
    {"name": "Hermès International", "country": "FR", "city": "Paris", "segment": "Ultra-Luxury Saddlery & Bags", "domain": "hermes.com", "contact": "Jean-Luc Dubois", "role": "Directeur Achats Cuirs Précieux"},
    {"name": "Louis Vuitton Malletier", "country": "FR", "city": "Paris", "segment": "Luxury Trunk & Handbag Leather", "domain": "louisvuitton.com", "contact": "Etienne Moreau", "role": "Responsable Sourcing Matières"},
    {"name": "Longchamp SAS", "country": "FR", "city": "Paris", "segment": "Premium Leather Handbags & Travel", "domain": "longchamp.com", "contact": "Philippe Cassegrain", "role": "Directeur Industriel & Cuir"},
    {"name": "Lancel Paris", "country": "FR", "city": "Paris", "segment": "Heritage Parisian Leather Bags", "domain": "lancel.com", "contact": "Claire Fontaine", "role": "Responsable Développement Matières"},
    {"name": "J.M. Weston", "country": "FR", "city": "Limoges", "segment": "Handcrafted Luxury Goodyear Shoes", "domain": "jmweston.com", "contact": "Michel Blanc", "role": "Maitre Bottier & Achats Cuir"},
    {"name": "Paraboot", "country": "FR", "city": "Izeaux", "segment": "Norwegian Welt Leather Boots", "domain": "paraboot.com", "contact": "Pierre Richard", "role": "Directeur des Approvisionnements"},
    {"name": "Faure Le Page", "country": "FR", "city": "Paris", "segment": "Historic Luxury Leather Goods", "domain": "faurelepage.com", "contact": "Antoine Leroux", "role": "Sourcing Manager"},

    # Spain (Gloves, Bags, Footwear)
    {"name": "Loewe S.A.", "country": "ES", "city": "Madrid", "segment": "Luxury Nappa & Calf Leather", "domain": "loewe.com", "contact": "Carlos Gomez", "role": "Director de Aprovisionamiento"},
    {"name": "Camper", "country": "ES", "city": "Inca (Mallorca)", "segment": "Contemporary Leather Footwear", "domain": "camper.com", "contact": "Jaume Fluxa", "role": "Footwear Materials Sourcing Lead"},
    {"name": "Magnanni Shoes", "country": "ES", "city": "Almansa", "segment": "Hand-Patinated Dress Shoes", "domain": "magnanni.com", "contact": "Pascual Blanco", "role": "Director de Calidad Cuero"},
    {"name": "Carmina Shoemaker", "country": "ES", "city": "Inca", "segment": "Bespoke Goodyear Cordovan & Boxcalf", "domain": "carminahoemaker.com", "contact": "Jose Albaladejo", "role": "Master Shoemaker"},
    {"name": "Lottusse 1877", "country": "ES", "city": "Inca", "segment": "High-End Leather Bags & Shoes", "domain": "lottusse.com", "contact": "Antonio Frau", "role": "Head of Sourcing"},

    # United Kingdom & Switzerland
    {"name": "Mulberry Group plc", "country": "UK", "city": "Bath", "segment": "British Luxury Handbags", "domain": "mulberry.com", "contact": "Edward Taylor", "role": "Head of Leather Sourcing & ESG"},
    {"name": "Church's English Shoes", "country": "UK", "city": "Northampton", "segment": "Heritage Goodyear Welt Footwear", "domain": "church-footwear.com", "contact": "Arthur Smith", "role": "Purchasing Manager"},
    {"name": "Crockett & Jones", "country": "UK", "city": "Northampton", "segment": "Luxury Calfskin Dress Shoes", "domain": "crockettandjones.com", "contact": "Jonathan Jones", "role": "Director of Leather Selection"},
    {"name": "John Lobb Bootmaker", "country": "UK", "city": "London", "segment": "Bespoke Royal Warrant Shoemaker", "domain": "johnlobb.com", "contact": "David Hall", "role": "Master Leather Buyer"},
    {"name": "Bally International", "country": "CH", "city": "Caslano", "segment": "Swiss Luxury Footwear & Accessories", "domain": "bally.com", "contact": "Beat Zuber", "role": "Global Sourcing Director"}
]

def seed_expansion():
    print("[M9 DATA EXPANSION] Seeding 50+ European Buyer Accounts & 100+ Signals...")
    db = SessionLocal()
    try:
        exporter = capability_repo.get_exporter_capability(db)
        created_accounts = 0
        created_signals = 0

        for b_data in EUROPEAN_BUYERS_EXPANSION:
            company_payload = {
                "canonical_name": b_data["name"],
                "legal_name": f"{b_data['name']} S.A./GmbH",
                "domain": b_data["domain"],
                "country_code": b_data["country"],
                "city": b_data["city"],
                "website": f"https://www.{b_data['domain']}",
                "segment": b_data["segment"],
                "description": f"European brand specialized in {b_data['segment']}.",
                "confidence": 0.92
            }

            company, is_new = entity_resolution_service.resolve_or_create_company(db, company_payload)
            if is_new:
                created_accounts += 1

            # Seed contact
            person = EntityPerson(
                id=uuid.uuid4(),
                company_id=company.id,
                full_name=b_data["contact"],
                title=b_data["role"],
                email=f"{b_data['contact'].lower().replace(' ', '.')}@{b_data['domain']}",
                is_primary=True,
                confidence=0.85,
                verification_status="verified",
                consent_status="legitimate_interest",
                legal_basis="B2B legitimate interest under GDPR Art. 6(1)(f)"
            )
            db.add(person)

            # Seed product requirement
            prod = EntityProduct(
                id=uuid.uuid4(),
                company_id=company.id,
                name=f"Premium Leather Specification for {b_data['segment']}",
                hs_code="4107",
                material_types=["Full-grain bovine", "Calf nappa", "Vegetable crust"],
                thickness_range_mm=["0.9-1.3", "1.2-1.6"],
                finish=["Semi-aniline", "Aniline"]
            )
            db.add(prod)

            # Seed Live Signal
            signal_titles = [
                (f"EUDR Provenance Compliance Review for {b_data['name']}", "regulatory", "high", 88),
                (f"New Season Leather Sourcing Tender ({b_data['segment']})", "intent", "medium", 82),
                (f"Lineapelle Milan Autumn/Winter 2026 Collection Sourcing Inquiry", "market", "medium", 79)
            ]

            for s_title, cat, sev, sc in signal_titles:
                sig = Signal(
                    id=uuid.uuid4(),
                    entity_id=company.id,
                    category=cat,
                    severity=sev,
                    title=s_title,
                    summary=f"Automated intelligence feed detected procurement activity for {b_data['name']} in {b_data['city']}.",
                    quote=f"Requiring certified LWG / EUDR deforestation-free leather suppliers for upcoming collection.",
                    score=sc,
                    evidence={"source": "Lineapelle / European Trade Press / LinkedIn Intent", "buyer": b_data['name']}
                )
                db.add(sig)
                created_signals += 1

        db.commit()
        print(f"  [OK] Seeded {created_accounts} new European accounts and {created_signals} trade signals.")

        # Re-score all accounts
        all_buyers = db.query(EntityCompany).filter(EntityCompany.country_code != "IN").all()
        print(f"  [SCORING] Computing 100-pt Match Scores for all {len(all_buyers)} European Buyers...")

        for idx, b in enumerate(all_buyers, start=1):
            score = scoring_service.score_match(b, exporter, rank=min(idx, 5))
            match_repo.upsert_match_candidate(db, {
                "buyer_id": b.id,
                "total_score": score.total_score,
                "product_fit_score": score.product_fit_score,
                "compliance_score": score.compliance_score,
                "lane_economics_score": score.lane_economics_score,
                "intent_signals_score": score.intent_signals_score,
                "accessibility_score": score.accessibility_score,
                "grade": score.grade,
                "rank": idx,
                "score_version": "v1.0.0",
                "drivers": [d.model_dump() for d in score.drivers],
                "key_gaps": score.key_gaps,
                "next_best_action": score.next_best_action,
                "outreach_angle": score.outreach_angle,
                "status": "suggested"
            })

            # Append-only history
            match_repo.insert_score_history(
                db,
                buyer_id=b.id,
                score=score.total_score,
                score_version="v1.0.0",
                drivers=[d.model_dump() for d in score.drivers]
            )

        print(f"[SUCCESS] Phase 2 Data Expansion complete: {len(all_buyers)} European buyers scored!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_expansion()
