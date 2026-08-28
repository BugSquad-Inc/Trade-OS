import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/api/ingest.ts
w("frontend/src/api/ingest.ts", """import { fetchApi } from './client';

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
""")

# 2. frontend/src/hooks/useIngest.ts
w("frontend/src/hooks/useIngest.ts", """import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getIngestionStatus, triggerPipelineRefresh } from '../api/ingest';

export function useIngestionStatus() {
  return useQuery({
    queryKey: ['ingestion-status'],
    queryFn: getIngestionStatus,
    refetchInterval: 15000,
  });
}

export function usePipelineRefresh() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: triggerPipelineRefresh,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['matches'] });
      queryClient.invalidateQueries({ queryKey: ['signals'] });
      queryClient.invalidateQueries({ queryKey: ['account'] });
      queryClient.invalidateQueries({ queryKey: ['ingestion-status'] });
    },
  });
}
""")
