import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export type OpportunityStage =
  | 'matched'
  | 'pitch_drafted'
  | 'outreach_sent'
  | 'reply_positive'
  | 'sample_requested'
  | 'sample_sent'
  | 'sample_approved'
  | 'quote_sent'
  | 'contract_negotiation'
  | 'po_received'
  | 'in_production'
  | 'closed_won'
  | 'closed_lost';

export interface Quote {
  id: string;
  opportunity_id: string;
  quote_number: string;
  quantity_sqft: number;
  unit_price_inr: number;
  unit_price_eur: number;
  fx_rate_eur_inr: number;
  estimated_freight_usd: number;
  customs_duty_pct: number;
  insurance_usd: number;
  landed_cost_eur_per_sqft: number;
  gross_margin_pct: number;
  total_quote_value_eur: number;
  payment_terms: string;
  lead_time_days: number;
  status: string;
  valid_until: string;
  created_at: string;
}

export interface Opportunity {
  id: string;
  buyer_id: string;
  product_family_id?: string;
  product_version_id?: string;
  title: string;
  stage: OpportunityStage;
  deal_value_eur: number;
  deal_value_inr: number;
  volume_sqft: number;
  incoterms: string;
  target_close_date?: string;
  probability: number;
  owner: string;
  loss_reason?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  quotes: Quote[];
}

export interface PipelineSummary {
  total_active_deals: number;
  total_pipeline_eur: number;
  total_won_eur: number;
  stage_counts: Record<string, number>;
}

export interface LandedCostCalculation {
  unit_price_inr: number;
  fx_rate_eur_inr: number;
  base_eur_per_sqft: number;
  freight_eur_per_sqft: number;
  insurance_eur_per_sqft: number;
  duty_eur_per_sqft: number;
  landed_cost_eur_per_sqft: number;
  recommended_unit_price_eur: number;
  total_quote_value_eur: number;
  total_quote_value_inr: number;
  gross_margin_pct: number;
  quantity_sqft: number;
}

export function useDeals(stage?: string) {
  const queryParam = stage ? `?stage=${stage}` : '';
  return useQuery<Opportunity[]>({
    queryKey: ['deals', stage],
    queryFn: () => fetchApi<Opportunity[]>(`/api/v1/deals${queryParam}`),
  });
}

export function usePipelineSummary() {
  return useQuery<PipelineSummary>({
    queryKey: ['pipeline_summary'],
    queryFn: () => fetchApi<PipelineSummary>('/api/v1/deals/summary/pipeline'),
  });
}

export function useUpdateDealStage() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ oppId, stage, notes }: { oppId: string; stage: OpportunityStage; notes?: string }) =>
      fetchApi<Opportunity>(`/api/v1/deals/${oppId}/stage`, {
        method: 'PATCH',
        body: JSON.stringify({ stage, notes }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
      queryClient.invalidateQueries({ queryKey: ['pipeline_summary'] });
      queryClient.invalidateQueries({ queryKey: ['today_cockpit'] });
    },
  });
}

export function useCalculateLandedCost() {
  return useMutation({
    mutationFn: (data: {
      unit_price_inr: number;
      quantity_sqft?: number;
      freight_usd?: number;
      insurance_usd?: number;
      customs_duty_pct?: number;
      target_margin_pct?: number;
      fx_rate_eur_inr?: number;
    }) =>
      fetchApi<LandedCostCalculation>('/api/v1/deals/calculator/landed-cost', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
  });
}

export function useIssueQuote() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ oppId, data }: { oppId: string; data: any }) =>
      fetchApi<Quote>(`/api/v1/deals/${oppId}/quotes`, {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
      queryClient.invalidateQueries({ queryKey: ['pipeline_summary'] });
      queryClient.invalidateQueries({ queryKey: ['today_cockpit'] });
    },
  });
}
