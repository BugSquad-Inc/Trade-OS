from typing import Dict, Any, List

class OutreachSequenceAgent:
    """Generates 3-step multi-channel export outreach sequence."""
    @staticmethod
    def run(buyer: Any, exporter: Any) -> List[Dict[str, Any]]:
        b_name = getattr(buyer, "canonical_name", "Buyer")
        e_name = getattr(exporter, "company_name", "Butler's Leather")
        return [
            {
                "step": 1,
                "channel": "Email",
                "timing": "Day 1",
                "subject": f"EUDR-Ready Leather Supply & Swatch Pack for {b_name}",
                "summary": "Introduce LWG Gold tannery capabilities, EUDR readiness, and request delivery address for physical swatch pack."
            },
            {
                "step": 2,
                "channel": "LinkedIn InMail",
                "timing": "Day 4",
                "subject": f"Connecting regarding Chennai-Hamburg ocean freight & {b_name} leather supply",
                "summary": "Connect with Head of Leather Procurement referencing recent seasonal collection expansion."
            },
            {
                "step": 3,
                "channel": "Technical Follow-Up",
                "timing": "Day 8",
                "subject": f"Technical Data Sheet & Eurofins REACH Declaration for {b_name}",
                "summary": "Share ISO 3377-2 tensile test results and proposed container trial pricing."
            }
        ]
