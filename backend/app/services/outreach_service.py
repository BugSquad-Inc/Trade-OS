from sqlalchemy.orm import Session
import uuid
from typing import Dict, Any
from app.repositories import account_repo, capability_repo, outreach_repo

def generate_personalized_outreach(db: Session, buyer_id: uuid.UUID, tone: str = "Professional", contact_name: str = None) -> Dict[str, Any]:
    company = account_repo.get_company_by_id(db, buyer_id)
    if not company:
        raise ValueError(f"Company {buyer_id} not found")

    exporter = capability_repo.get_exporter_capability(db)
    exporter_name = exporter.company_name if exporter else "Butler's Leather"
    primary_contact = next((p for p in company.persons if p.is_primary), company.persons[0] if company.persons else None)
    target_name = contact_name or (primary_contact.full_name if primary_contact else "Sourcing Team")
    target_title = primary_contact.title if primary_contact else "Head of Leather Procurement"

    templates = {
        "Professional": {
            "subject": f"EUDR-Ready Leather Supply Partnership — {exporter_name} / {company.canonical_name}",
            "body": f"""Dear {target_name},

I am writing to you from {exporter_name}, an LWG Gold-certified tannery based in the Chennai/Ambur leather cluster in India.

We have followed {company.canonical_name}'s emphasis on premium craftsmanship and supply chain transparency. With EUDR enforcement approaching, we have structured our export supply chain to provide lot-level traceability, deforestation-free declarations, and full REACH SVHC chemical test documentation.

Our facility currently exports finished bovine and goat leather (0.8–2.2mm) with direct ocean transit from Chennai Port to Hamburg (26–34 days) at competitive landed economics.

We would welcome the opportunity to courier a tailored swatch pack (3–5 articles) directly to your product development team in {company.city or 'Germany'}.

Would you be open to a brief 10-minute introductory call next week?

Best regards,
Sourcing & Export Team
{exporter_name} | Chennai, India
"""
        },
        "Direct": {
            "subject": f"Finished Leather Supply & EUDR Due Diligence Package for {company.canonical_name}",
            "body": f"""Hi {target_name},

Reaching out directly regarding {company.canonical_name}'s finished leather procurement.

{exporter_name} (Chennai, India) provides:
• LWG Gold Rated finished bovine & goat leather (0.9–1.4mm uppers / lining)
• 68/100 EUDR Due Diligence Readiness with full compliance documentation pack
• 3,000 sq ft MOQ with 30-day production lead time
• Direct Chennai → Hamburg ocean corridor ($1,850/FEU spot benchmark)

Can we dispatch sample swatches to your {company.city or 'German'} facility this week?

Regards,
Export Desk
{exporter_name}
"""
        },
        "Technical": {
            "subject": f"Technical Spec & REACH/EUDR Test Matrix — {exporter_name} -> {company.canonical_name}",
            "body": f"""Dear {target_name},

Regarding technical material specifications for {company.canonical_name}:

{exporter_name} manufactures finished leather with the following certified technical parameters:
• Tensile Strength: >20 N/mm² | Tear Strength: >40 N (ISO 3377-2)
• Chromium VI: Non-detectable (<3 ppm) | Azo Dyes: Non-detectable (<30 ppm)
• Finish: Semi-aniline / Pigmented with ISO 11640 dry/wet rub fastness Grade 4/5
• EUDR Compliance: Article 9 due diligence statement & batch geolocation mapping available

We have pre-matched your {company.segment} product catalog and prepared a technical data sheet pack.

Please let us know where to courier the physical sample ring.

Sincerely,
Quality & Technical Director
{exporter_name}
"""
        },
        "Relationship": {
            "subject": f"Connecting regarding European leather trade & sustainable supply with {company.canonical_name}",
            "body": f"""Dear {target_name},

{exporter_name} has been crafting fine leathers in the Chennai cluster for over two decades. We deeply admire {company.canonical_name}'s heritage and dedication to high-quality leather goods.

As European sourcing requirements evolve around EUDR and sustainability, we are partnering closely with select German brands to provide reliable, long-term leather supply with verified provenance.

We would love to introduce ourselves and share a few curated swatches that align with your upcoming collection runs.

Warm regards,
Managing Director
{exporter_name}
"""
        }
    }

    selected = templates.get(tone, templates["Professional"])

    # Log action to gold.actions
    action_log = outreach_repo.log_outreach_action(
        db,
        buyer_id=buyer_id,
        action_type="outreach_generation",
        payload={"tone": tone, "contact": target_name, "subject": selected["subject"]}
    )

    return {
        "action_id": str(action_log.id),
        "buyer_id": str(buyer_id),
        "buyer_name": company.canonical_name,
        "contact_name": target_name,
        "contact_title": target_title,
        "tone": tone,
        "subject": selected["subject"],
        "body": selected["body"],
        "status": "generated"
    }
