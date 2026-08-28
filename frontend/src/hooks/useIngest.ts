import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
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
