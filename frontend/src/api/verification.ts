import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export interface VerificationItem {
  id: string;
  entity_id: string;
  entity_type: string;
  entity_name: string;
  claim_type: string;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'in_review' | 'verified' | 'rejected';
  assigned_to?: string;
  evidence_summary?: string;
  notes?: string;
  created_at: string;
  completed_at?: string;
}

export interface EntityResolutionLink {
  id: string;
  source_entity_id: string;
  target_entity_id: string;
  link_type: string;
  confidence: number;
  evidence: Record<string, any>;
  reviewer?: string;
  status: string;
  created_at: string;
}

export interface CorrectionRecord {
  id: string;
  entity_id: string;
  entity_type: string;
  field_name: string;
  old_value?: string;
  new_value: string;
  reason: string;
  reporter_email: string;
  status: string;
  created_at: string;
}

export function useVerificationQueue(statusFilter?: string) {
  const queryParam = statusFilter ? `?status=${statusFilter}` : '';
  return useQuery<VerificationItem[]>({
    queryKey: ['verification_queue', statusFilter],
    queryFn: () => fetchApi<VerificationItem[]>(`/api/v1/verification/queue${queryParam}`),
  });
}

export function useSignOffClaim() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      queueId,
      approved,
      notes,
    }: {
      queueId: string;
      approved: boolean;
      notes?: string;
    }) =>
      fetchApi<VerificationItem>(`/api/v1/verification/queue/${queueId}/sign-off`, {
        method: 'POST',
        body: JSON.stringify({ approved, notes }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['verification_queue'] });
      queryClient.invalidateQueries({ queryKey: ['matches'] });
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
    },
  });
}

export function useSubmitCorrection() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      entity_id: string;
      field_name: string;
      new_value: string;
      reason: string;
      old_value?: string;
    }) =>
      fetchApi<CorrectionRecord>('/api/v1/verification/corrections', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['verification_queue'] });
    },
  });
}

export function useEntityResolutionLinks() {
  return useQuery<EntityResolutionLink[]>({
    queryKey: ['entity_resolution_links'],
    queryFn: () => fetchApi<EntityResolutionLink[]>('/api/v1/verification/entity-resolution'),
  });
}
