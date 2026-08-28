import { fetchApi } from './client';

export interface ActivationKPIs {
  profile_completeness_pct: number;
  dossier_completeness_pct: number;
  match_explainability_pct: number;
  verified_contacts_count: number;
}

export interface GTMKPIs {
  total_buyers_monitored: number;
  grade_a_matches: number;
  grade_b_matches: number;
  active_signals_count: number;
  total_customs_teu: number;
  enterprise_mrr_pipeline_usd: number;
}

export interface ExecutiveKPIDashboardResponse {
  timestamp: string;
  active_exporter: string;
  exporter_origin: string;
  activation: ActivationKPIs;
  gtm: GTMKPIs;
  recent_agent_runs: number;
  crm_exports_count: number;
}

export const getExecutiveKPIsApi = () =>
  fetchApi<ExecutiveKPIDashboardResponse>('/api/v1/analytics/kpis');
