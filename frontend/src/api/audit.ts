import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export type AuditCategory =
  | 'AUTH'
  | 'ACCESS'
  | 'MODIFICATION'
  | 'EXPORT_DATA'
  | 'COMPLIANCE_SIGN_OFF'
  | 'FINANCE_MODIFICATION';

export interface AuditEventRecord {
  id: string;
  tenant_id?: string;
  user_id?: string;
  event_category: AuditCategory;
  action: string;
  entity_type: string;
  entity_id?: string;
  actor_email: string;
  ip_address: string;
  user_agent: string;
  payload_diff: Record<string, any>;
  created_at: string;
}

export interface AuditStatsResponse {
  total_audit_events: number;
  compliance_sign_offs: number;
  financial_modifications: number;
  security_access_events: number;
  tamper_evident_status: string;
}

export function useAuditEvents(category?: string, entityType?: string) {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (entityType) params.append('entity_type', entityType);
  const queryStr = params.toString() ? `?${params.toString()}` : '';

  return useQuery<AuditEventRecord[]>({
    queryKey: ['audit_events', category, entityType],
    queryFn: () => fetchApi<AuditEventRecord[]>(`/api/v1/audit/events${queryStr}`),
  });
}

export function useAuditStats() {
  return useQuery<AuditStatsResponse>({
    queryKey: ['audit_stats'],
    queryFn: () => fetchApi<AuditStatsResponse>('/api/v1/audit/stats'),
  });
}

export function useLogAuditEvent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<AuditEventRecord>) =>
      fetchApi<AuditEventRecord>('/api/v1/audit/events', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['audit_events'] });
      queryClient.invalidateQueries({ queryKey: ['audit_stats'] });
    },
  });
}
