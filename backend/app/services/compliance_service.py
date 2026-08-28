from typing import Dict, Any, List

def calculate_eudr_readiness(exporter_capability: Any) -> Dict[str, Any]:
    score = getattr(exporter_capability, "eudr_readiness_score", 68)
    checklist = [
        {"item": "Deforestation-Free Production Verification (Cut-off Dec 31, 2020)", "status": "verified", "article": "Article 3(a)"},
        {"item": "Standardized Due Diligence Statement (DDS) Template", "status": "verified", "article": "Article 4(2)"},
        {"item": "LWG Audit & Chemical Test Documentation Pack", "status": "verified", "article": "Article 9(1)"},
        {"item": "Farm / Slaughterhouse Geolocation Polygons", "status": "gap", "article": "Article 9(1)(d)", "gap_detail": "Missing geolocation for ~30% smallholder hide supply cluster"}
    ]
    return {
        "entity": getattr(exporter_capability, "company_name", "Butler's Leather"),
        "readiness_score": score,
        "status": "partial",
        "requirements": checklist,
        "top_gap": "Farm-level GPS polygon coordinates for raw hide provenance",
        "recommended_action": "Deploy smallholder supplier mobile GPS polygon upload portal"
    }

def calculate_reach_compliance(certifications: List[Any]) -> Dict[str, Any]:
    has_reach = any("reach" in getattr(c, "certification_type", "").lower() or "reach" in getattr(c, "certification_name", "").lower() for c in certifications)
    return {
        "status": "compliant" if has_reach else "pending_review",
        "restricted_substances_tested": ["Chromium VI (<3 ppm)", "Azo Dyes (<30 ppm)", "PCP (<0.5 ppm)", "Formaldehyde (<20 ppm)"],
        "test_lab": "TUV Rheinland / Eurofins Verified",
        "valid_until": "2026-12-31"
    }
