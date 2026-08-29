import uuid
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.exporter import ExporterCapability

def get_exporter_profile(db: Session) -> Optional[ExporterCapability]:
    """Retrieve primary exporter capability profile."""
    stmt = select(ExporterCapability).limit(1)
    return db.execute(stmt).scalar_one_or_none()

def upsert_exporter_profile(db: Session, data: Dict[str, Any]) -> ExporterCapability:
    """Create or update exporter profile with onboarding and registration details."""
    profile = get_exporter_profile(db)
    if not profile:
        profile = ExporterCapability(**data)
        db.add(profile)
    else:
        for k, v in data.items():
            if hasattr(profile, k):
                setattr(profile, k, v)
    db.commit()
    db.refresh(profile)
    return profile

def update_onboarding_step(db: Session, step: int, step_data: Dict[str, Any]) -> ExporterCapability:
    """Update step data and progress for exporter onboarding wizard."""
    profile = get_exporter_profile(db)
    if not profile:
        profile = ExporterCapability(
            company_name=step_data.get("company_name", "My Tannery Export Corp"),
            location=step_data.get("location", "Chennai, India"),
            cluster=step_data.get("cluster", "Ambur / Ranipet Cluster"),
            onboarding_step=step,
            **step_data
        )
        db.add(profile)
    else:
        profile.onboarding_step = max(profile.onboarding_step, step)
        for k, v in step_data.items():
            if hasattr(profile, k):
                setattr(profile, k, v)
    db.commit()
    db.refresh(profile)
    return profile

def get_readiness_gap_analysis(db: Session) -> Dict[str, Any]:
    """Calculate missing commercial and regulatory readiness items for Indian exporters."""
    profile = get_exporter_profile(db)
    if not profile:
        return {
            "status": "uninitialized",
            "overall_score": 0,
            "missing_mandatory": ["company_name", "pan", "gstin", "iec", "ad_code"],
            "missing_recommended": ["rcmc_number", "lut_status", "lwg_certification"],
            "remediation_tasks": []
        }

    mandatory_checks = {
        "PAN Tax Registration": bool(profile.pan),
        "GSTIN Export Registration": bool(profile.gstin_list and len(profile.gstin_list) > 0),
        "IEC (Import Export Code)": bool(profile.iec),
        "AD Code (Bank Remittance Registration)": bool(profile.ad_code),
        "ICEGATE Customs Registration": profile.icegate_status == "registered"
    }

    recommended_checks = {
        "RCMC Membership (Council for Leather Exports)": bool(profile.rcmc_number),
        "Active LUT (Letter of Undertaking for Zero-Rated Exports)": profile.lut_status == "active",
        "LWG Gold/Silver Environmental Certification": any("LWG" in str(c) for c in (profile.certifications or [])),
        "REACH Chemical Compliance Declaration": any("REACH" in str(c) for c in (profile.certifications or []))
    }

    missing_mandatory = [k for k, v in mandatory_checks.items() if not v]
    missing_recommended = [k for k, v in recommended_checks.items() if not v]

    passed_count = sum(mandatory_checks.values()) * 15 + sum(recommended_checks.values()) * 6.25
    overall_score = min(100, int(passed_count))

    tasks = []
    for item in missing_mandatory:
        tasks.append({
            "priority": "HIGH",
            "title": f"Complete {item}",
            "remediation": "Upload official certificate or register via DGFT / ICEGATE portal",
            "status": "pending"
        })
    for item in missing_recommended:
        tasks.append({
            "priority": "MEDIUM",
            "title": f"Obtain / Link {item}",
            "remediation": "Attach lab test report or membership renewal document",
            "status": "pending"
        })

    return {
        "status": profile.onboarding_status,
        "overall_score": overall_score,
        "mandatory_checks": mandatory_checks,
        "recommended_checks": recommended_checks,
        "missing_mandatory": missing_mandatory,
        "missing_recommended": missing_recommended,
        "remediation_tasks": tasks,
        "reviewed_by": profile.reviewed_by,
        "reviewed_at": profile.reviewed_at
    }
