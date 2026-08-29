import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';
import { PipelineSummary } from './deals';

export interface TaskItem {
  id: string;
  opportunity_id?: string;
  buyer_id?: string;
  title: string;
  description?: string;
  due_date: string;
  priority: 'urgent' | 'high' | 'medium' | 'low';
  status: 'todo' | 'in_progress' | 'completed';
  task_type: string;
  assigned_to: string;
  created_at: string;
  completed_at?: string;
}

export interface RecommendedAction {
  priority: string;
  type: string;
  title: string;
  description: string;
  target: string;
  est_deal_value_eur: number;
}

export interface TodayCockpitData {
  date: string;
  exporter_name: string;
  readiness_score: number;
  urgent_tasks: TaskItem[];
  pipeline_summary: PipelineSummary;
  recommended_actions: RecommendedAction[];
}

export function useTodayCockpit() {
  return useQuery<TodayCockpitData>({
    queryKey: ['today_cockpit'],
    queryFn: () => fetchApi<TodayCockpitData>('/api/v1/today'),
  });
}

export function useCompleteTask() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (taskId: string) =>
      fetchApi<TaskItem>(`/api/v1/today/tasks/${taskId}/complete`, {
        method: 'POST',
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['today_cockpit'] });
    },
  });
}
