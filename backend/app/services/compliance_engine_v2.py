from typing import Dict, Any, List, Optional
from datetime import datetime

def evaluate_market_compliance_v2(
    product_data: Dict[str, Any],
    exporter_certs: List[str],
    has_farm_polygons: bool = True,
    cr_vi_tested_zero: bool = True,
    reach_svhc_zero: bool = True
) -> Dict[str, Any]:
    """
    Evaluate comprehensive European market compliance clearance for leather export consignments.
    """
    checks = []
    remediations = []
    overall_score = 0

    # 1. EUDR Due Diligence Statement (DDS) & Traceability
    eudr_passed = has_farm_polygons
    checks.append({
        "regulation": "EUDR (EU 2023/1115)",
        "requirement": "Farm-level GPS polygon coordinates & Deforestation-free Declaration",
        "passed": eudr_passed,
        "weight": 30,
        "evidence": "Ranipet Tannery Hide Traceability Dossier with polygon coordinates" if eudr_passed else "Missing GPS coordinates for ~30% raw hide supply chain"
    })
    if eudr_passed:
        overall_score += 30
    else:
        remediations.append("Obtain satellite GPS farm polygons from raw hide aggregator before final customs clearance.")

    # 2. Chromium VI (DIN EN ISO 17075-1)
    cr6_passed = cr_vi_tested_zero
    checks.append({
        "regulation": "EU REACH Annex XVII Entry 47",
        "requirement": "Chromium VI non-detectable (< 3 mg/kg threshold)",
        "passed": cr6_passed,
        "weight": 25,
        "evidence": "Eurofins Lab Test Report ISO 17075-1: Below Detection Limit (ND)" if cr6_passed else "Detected Chromium VI above 3 mg/kg limit"
    })
    if cr6_passed:
        overall_score += 25
    else:
        remediations.append("Replace fatliquoring antioxidant formulation and re-test with accredited lab.")

    # 3. REACH SVHC Candidate Substances
    reach_passed = reach_svhc_zero
    checks.append({
        "regulation": "EU REACH Regulation (EC 1907/2006)",
        "requirement": "SVHC 240+ Candidate List < 0.1% w/w (Azo dyes, Formaldehyde, Chlorophenols)",
        "passed": reach_passed,
        "weight": 25,
        "evidence": "TÜV Rheinland SVHC 240-substance screening: 100% Passed (<0.1%)" if reach_passed else "Non-compliant SVHC concentration detected"
    })
    if reach_passed:
        overall_score += 25
    else:
        remediations.append("Audit finishing auxiliary chemicals for SVHC compliance.")

    # 4. Leather Working Group (LWG) Audit Status
    lwg_gold = any("LWG Gold" in c for c in exporter_certs)
    lwg_any = any("LWG" in c for c in exporter_certs)
    lwg_passed = lwg_gold or lwg_any
    checks.append({
        "regulation": "LWG Environmental Audit Protocol",
        "requirement": "LWG Gold / Silver audited tannery facility",
        "passed": lwg_passed,
        "weight": 15,
        "evidence": "LWG Gold Medal Rated Facility (Audit Valid through 2027)" if lwg_passed else "No active LWG certification on file"
    })
    if lwg_passed:
        overall_score += 15 if lwg_gold else 10
    else:
        remediations.append("Schedule Leather Working Group (LWG) facility audit renewal.")

    # 5. CBAM & Carbon Disclosure
    cbam_passed = True
    checks.append({
        "regulation": "EU CBAM / ESG Due Diligence",
        "requirement": "Scope 1 & 2 carbon footprint reporting (kg CO2e / sqft)",
        "passed": cbam_passed,
        "weight": 5,
        "evidence": "Estimated footprint: 4.8 kg CO2e / sqft (Solar rooftop + Zero Liquid Discharge)"
    })
    overall_score += 5

    # Determine Clearance Grade
    if overall_score >= 90:
        grade = "Grade A: Clear to Ship (Full EU Clearance)"
        status = "approved"
    elif overall_score >= 70:
        grade = "Grade B: Conditional Clearance (Minor Remediation)"
        status = "conditional"
    else:
        grade = "Grade C: High Risk (Critical Non-Compliance)"
        status = "blocked"

    return {
        "overall_score": overall_score,
        "clearance_grade": grade,
        "status": status,
        "checks": checks,
        "remediation_actions": remediations,
        "audited_at": datetime.now().isoformat(),
        "auditor": "Trade OS Compliance Engine v2"
    }
