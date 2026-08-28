import { fetchApi } from './client';

export interface AgentStepResult {
  agent_name: string;
  status: string;
  output: Record<string, any>;
  execution_time_ms: number;
}

export interface AgentWorkflowResponse {
  workflow_id: string;
  buyer_id: string;
  buyer_name: string;
  status: string;
  completed_steps: AgentStepResult[];
  approval_required: boolean;
  summary_action_plan: string;
}

export const executeAgentsApi = (buyerId: string) =>
  fetchApi<AgentWorkflowResponse>('/api/v1/agents/execute', {
    method: 'POST',
    body: JSON.stringify({ buyer_id: buyerId, requires_human_approval: true }),
  });
