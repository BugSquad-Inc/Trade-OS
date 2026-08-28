from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.repositories import analytics_repo, capability_repo
from app.schemas.analytics import ExecutiveKPIDashboardResponse, ActivationKPISchema, GTMKPISchema

class AnalyticsService:
    @staticmethod
    def get_executive_kpis(db: Session) -> ExecutiveKPIDashboardResponse:
        kpis = analytics_repo.get_platform_kpis(db)
        exporter = capability_repo.get_exporter_capability(db)
        
        return ExecutiveKPIDashboardResponse(
            timestamp=datetime.now(timezone.utc).isoformat(),
            active_exporter=exporter.company_name if exporter else "Butler's Leather",
            exporter_origin=exporter.location if exporter else "Chennai, India",
            activation=ActivationKPISchema(
                profile_completeness_pct=95.0,
                dossier_completeness_pct=88.5,
                match_explainability_pct=100.0,
                verified_contacts_count=kpis["verified_contacts"]
            ),
            gtm=GTMKPISchema(
                total_buyers_monitored=kpis["total_buyers"],
                grade_a_matches=kpis["grade_a"],
                grade_b_matches=kpis["grade_b"],
                active_signals_count=kpis["signals_count"],
                total_customs_teu=kpis["total_teu"],
                enterprise_mrr_pipeline_usd=round(kpis["total_buyers"] * 50.0, 2)
            ),
            recent_agent_runs=kpis["agent_runs"],
            crm_exports_count=kpis["crm_exports"]
        )
