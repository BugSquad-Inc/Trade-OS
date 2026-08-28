import uuid
import io
import csv
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.repositories import account_repo, match_repo, capability_repo, crm_repo
from app.services import outreach_service

class CRMExportService:
    """Generates enterprise exports for HubSpot, Salesforce, and CSV."""

    @staticmethod
    def export_buyer_dossier(
        db: Session,
        buyer_id: uuid.UUID,
        export_format: str = "hubspot"
    ) -> Dict[str, Any]:
        company = account_repo.get_company_by_id(db, buyer_id)
        if not company:
            raise ValueError("Buyer not found")

        exporter = capability_repo.get_exporter_capability(db)
        match = match_repo.get_match_by_buyer_id(db, buyer_id)
        outreach_data = outreach_service.generate_personalized_outreach(db, buyer_id, tone="Professional")
        outreach_subject = outreach_data.get("subject", "EUDR Leather Supply Partnership")
        outreach_body = outreach_data.get("body", "")

        primary_contact = next((c for c in company.persons if c.is_primary), company.persons[0] if company.persons else None)

        if export_format.lower() == "hubspot":
            payload = {
                "company_properties": {
                    "name": company.canonical_name,
                    "domain": company.domain,
                    "city": company.city,
                    "country": company.country_code,
                    "tradeos_match_score": float(match.total_score) if match else 85.0,
                    "tradeos_match_grade": match.grade if match else "A",
                    "tradeos_target_segment": company.segment,
                    "tradeos_eudr_readiness": "68/100 (Article 4 DDS Required)"
                },
                "contact_properties": {
                    "firstname": primary_contact.full_name.split()[0] if primary_contact else "Procurement",
                    "lastname": " ".join(primary_contact.full_name.split()[1:]) if primary_contact and len(primary_contact.full_name.split()) > 1 else "Lead",
                    "email": primary_contact.email if primary_contact else "",
                    "jobtitle": primary_contact.title if primary_contact else "Leather Sourcing Manager",
                    "gdpr_legal_basis": "B2B Legitimate Interest Art. 6(1)(f)"
                },
                "deal_proposal": {
                    "dealname": f"Butler's Leather → {company.canonical_name} (Trial Container)",
                    "pipeline": "Export Sales Pipeline",
                    "stage": "Qualified Match",
                    "amount": "45000",
                    "currency": "USD",
                    "initial_outreach_subject": outreach_subject,
                    "initial_outreach_body": outreach_body
                }
            }
        elif export_format.lower() == "salesforce":
            payload = {
                "Lead": {
                    "Company": company.canonical_name,
                    "FirstName": primary_contact.full_name.split()[0] if primary_contact else "Procurement",
                    "LastName": " ".join(primary_contact.full_name.split()[1:]) if primary_contact and len(primary_contact.full_name.split()) > 1 else "Lead",
                    "Email": primary_contact.email if primary_contact else "",
                    "Title": primary_contact.title if primary_contact else "Leather Sourcing Lead",
                    "Country": company.country_code,
                    "City": company.city,
                    "Status": "Working - Contacted",
                    "TradeOS_Score__c": float(match.total_score) if match else 85.0,
                    "Description": f"Export match: {company.segment}. Outreach Draft:\n{outreach_body}"
                }
            }
        else:  # CSV format
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Company Name", "Country", "City", "Match Score", "Grade", "Contact Name", "Contact Email", "Outreach Subject"])
            writer.writerow([
                company.canonical_name,
                company.country_code,
                company.city,
                float(match.total_score) if match else 85.0,
                match.grade if match else "A",
                primary_contact.full_name if primary_contact else "",
                primary_contact.email if primary_contact else "",
                outreach_subject
            ])
            payload = {"csv_content": output.getvalue()}

        # Log export
        log_entry = crm_repo.log_crm_export(db, buyer_id, export_format, payload)

        return {
            "export_id": str(log_entry.id),
            "buyer_id": str(buyer_id),
            "buyer_name": company.canonical_name,
            "format": export_format,
            "status": "success",
            "payload": payload,
            "message": f"Successfully generated {export_format.upper()} export payload for {company.canonical_name}."
        }
