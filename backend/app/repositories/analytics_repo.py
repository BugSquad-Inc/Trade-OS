from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from typing import Dict, Any
from app.models.company import EntityCompany, EntityPerson
from app.models.match import MatchCandidate
from app.models.signal import Signal
from app.models.customs import CustomsShipmentNormalized, CRMExportLog
from app.models.analytics import AgentRunRecord

def get_platform_kpis(db: Session) -> Dict[str, Any]:
    total_buyers = db.query(EntityCompany).filter(EntityCompany.country_code != "IN").count()
    verified_contacts = db.query(EntityPerson).filter(EntityPerson.verification_status == "verified").count()
    grade_a = db.query(MatchCandidate).filter(MatchCandidate.grade == "A").count()
    grade_b = db.query(MatchCandidate).filter(MatchCandidate.grade == "B").count()
    signals_count = db.query(Signal).count()
    
    teu_sum = db.query(func.coalesce(func.sum(CustomsShipmentNormalized.teu_count), 0.0)).scalar()
    crm_exports = db.query(CRMExportLog).count()
    agent_runs = db.query(AgentRunRecord).count()

    return {
        "total_buyers": total_buyers,
        "verified_contacts": verified_contacts,
        "grade_a": grade_a,
        "grade_b": grade_b,
        "signals_count": signals_count,
        "total_teu": float(teu_sum),
        "crm_exports": crm_exports,
        "agent_runs": agent_runs
    }
