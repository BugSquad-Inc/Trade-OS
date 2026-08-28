import { fetchApi } from './client';

export interface IngestionRunItem {
  id: string;
  source_name: string;
  status: string;
  started_at: string;
  finished_at?: string;
  stats: Record<string, any>;
  error?: string;
}

export interface IngestionStatusResponse {
  runs: IngestionRunItem[];
  total_runs: number;
  active_sources: number;
}

export interface PipelineRefreshResponse {
  status: string;
  message: string;
  buyers_scored: number;
  signals_updated: number;
  duration_ms: number;
}

export const getIngestionStatus = () => fetchApi<IngestionStatusResponse>('/api/v1/ingest/status');
export const triggerPipelineRefresh = () => fetchApi<PipelineRefreshResponse>('/api/v1/ingest/refresh', { method: 'POST' });
