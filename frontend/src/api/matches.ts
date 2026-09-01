import { fetchApi } from './client';

export interface DriverItem {
  category: string;
  weight: number;
  score: number;
  title: string;
  evidence: string;
}

export interface CounterFactualItem {
  action: string;
  dimension: string;
  score_impact_pts: number;
  projected_total_score: number;
  implementation_tip: string;
}

export interface MatchCard {
  id: string;
  buyer_id: string;
  name: string;
  legal_name: string;
  country_code: string;
  country: string;
  city: string;
  segment: string;
  rank: number;
  total_score: number;
  grade: string;
  score_version?: string;
  is_compliance_gate_failed?: boolean;
  compliance_gate_reason?: string;
  score_breakdown: {
    product_fit: number;
    compliance: number;
    lane_economics: number;
    intent_signals: number;
    accessibility: number;
  };
  drivers: DriverItem[];
  counter_factuals?: CounterFactualItem[];
  key_gaps: string[];
  next_best_action: string;
  outreach_angle: string;
  status: string;
  contact?: {
    full_name: string;
    title?: string;
    email?: string;
    confidence: number;
    verification_status: string;
  };
  freight_summary: string;
  eudr_readiness_score: number;
}

export interface MatchListResponse {
  matches: MatchCard[];
  total_count: number;
  generated_at: string;
  score_version?: string;
}

export const getMatches = () => fetchApi<MatchListResponse>('/api/v1/matches');
