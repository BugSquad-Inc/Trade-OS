import { fetchApi } from './client';

export interface SignalItem {
  id: string;
  entity_id: string;
  company_name: string;
  category: string;
  severity: string;
  title: string;
  summary: string;
  quote?: string;
  source_url?: string;
  detected_at: string;
  score: number;
  evidence: Record<string, any>;
}

export interface EUDRChecklistItem {
  item: string;
  status: string;
  article: string;
  gap_detail?: string;
}

export interface SignalListResponse {
  signals: SignalItem[];
  total_count: number;
  eudr_scorecard: {
    entity: string;
    readiness_score: number;
    status: string;
    requirements: EUDRChecklistItem[];
    top_gap: string;
    recommended_action: string;
  };
  freight_benchmark: {
    origin_port: string;
    destination_port: string;
    mode: string;
    container_type: string;
    rate_usd: number;
    rate_spread: string;
    transit_days: string;
    port_congestion_index: string;
    reroute_risk_notes?: string;
    sample_air_transit: string;
  };
}

export const getSignals = () => fetchApi<SignalListResponse>('/api/v1/signals');
