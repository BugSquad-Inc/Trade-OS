import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export interface JourneyActionDefinition {
  action_id: string;
  label: string;
  target_stage: string;
  target_macro_stage: string;
  required_role: string;
  requires_evidence: boolean;
  evidence_prompt?: string;
  description: string;
}

export interface BlockedActionDefinition {
  action_id: string;
  label: string;
  target_stage: string;
  blocked_reasons: string[];
  prerequisites: string[];
}

export interface StageEvent {
  id: string;
  entity_type: string;
  entity_id: string;
  macro_stage: string;
  previous_stage: string;
  new_stage: string;
  action: string;
  actor: string;
  actor_role: string;
  reason_code: string;
  notes?: string;
  evidence_references: Record<string, any>;
  created_at: string;
}

export interface JourneyState {
  entity_id: string;
  entity_type: string;
  current_stage: string;
  macro_stage: string;
  stage_title: string;
  owner_question: string;
  available_actions: JourneyActionDefinition[];
  blocked_actions: BlockedActionDefinition[];
  history: StageEvent[];
}

export interface TransitionRequest {
  action_id: string;
  actor?: string;
  actor_role?: string;
  reason_code?: string;
  notes?: string;
  evidence_references?: Record<string, any>;
  idempotency_key?: string;
}

export interface TransitionResponse {
  success: boolean;
  entity_id: string;
  previous_stage: string;
  new_stage: string;
  macro_stage: string;
  event_id: string;
  message: string;
  available_actions: JourneyActionDefinition[];
}

export function useJourneyState(oppId?: string) {
  return useQuery<JourneyState>({
    queryKey: ['journeyState', oppId],
    queryFn: () => fetchApi<JourneyState>(`/api/v1/journey/opportunities/${oppId}/state`),
    enabled: !!oppId,
  });
}

export function useJourneyHistory(oppId?: string) {
  return useQuery<StageEvent[]>({
    queryKey: ['journeyHistory', oppId],
    queryFn: () => fetchApi<StageEvent[]>(`/api/v1/journey/opportunities/${oppId}/history`),
    enabled: !!oppId,
  });
}

export function useExecuteTransition() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ oppId, req }: { oppId: string; req: TransitionRequest }) =>
      fetchApi<TransitionResponse>(`/api/v1/journey/opportunities/${oppId}/transition`, {
        method: 'POST',
        body: JSON.stringify(req),
      }),
    onSuccess: (_, { oppId }) => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
      queryClient.invalidateQueries({ queryKey: ['journeyState', oppId] });
      queryClient.invalidateQueries({ queryKey: ['journeyHistory', oppId] });
      queryClient.invalidateQueries({ queryKey: ['todayCockpit'] });
      queryClient.invalidateQueries({ queryKey: ['pipelineSummary'] });
    },
  });
}
