import { fetchApi } from './client';

export interface SearchResultItem {
  company_id: string;
  canonical_name: string;
  country_code: string;
  city?: string;
  segment: string;
  description?: string;
  dense_rank?: number;
  sparse_rank?: number;
  rrf_score: number;
  relevance_explanation: string;
  match_score?: number;
  grade?: string;
}

export interface HybridSearchResponse {
  query: string;
  total_results: number;
  results: SearchResultItem[];
  execution_time_ms: number;
}

export const hybridSearchApi = (query: string, country?: string) =>
  fetchApi<HybridSearchResponse>('/api/v1/search/hybrid', {
    method: 'POST',
    body: JSON.stringify({ query, target_country: country, top_k: 8 }),
  });
