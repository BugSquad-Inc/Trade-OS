import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export interface ExporterProfile {
  id: string;
  company_name: string;
  location: string;
  cluster: string;
  export_market_focus: string[];
  material_types: string[];
  tannage: string[];
  thickness_range_mm: string[];
  finish_capabilities: string[];
  monthly_capacity_sqft: number;
  moq_sqft: number;
  lead_time_days: number;
  sample_lead_time_days: number;
  port_of_export: string;
  incoterms: string[];
  certifications: string[];
  eudr_readiness_score: number;
  eudr_gap_summary?: string;

  pan?: string;
  gstin_list: string[];
  iec?: string;
  udyam_number?: string;
  rcmc_number?: string;
  rcmc_expiry?: string;
  lut_status?: string;
  lut_expiry?: string;
  ad_code?: string;
  ad_bank_branch?: string;
  ad_bank_ifsc?: string;
  icegate_status?: string;
  authorised_signatory?: string;
  facilities: Array<{ name: string; area_sqft?: number; workers?: number }>;
  ports: string[];
  incoterms_preference: string[];
  commercial_constraints?: string;

  onboarding_step: number;
  onboarding_status: string;
  reviewed_by?: string;
  reviewed_at?: string;
  evidence_status: Record<string, string>;
  created_at: string;
  updated_at: string;
}

export interface ReadinessGapAnalysis {
  status: string;
  overall_score: number;
  mandatory_checks: Record<string, boolean>;
  recommended_checks: Record<string, boolean>;
  missing_mandatory: string[];
  missing_recommended: string[];
  remediation_tasks: Array<{
    priority: 'HIGH' | 'MEDIUM' | 'LOW';
    title: string;
    remediation: string;
    status: string;
  }>;
  reviewed_by?: string;
  reviewed_at?: string;
}

export function useExporterProfile() {
  return useQuery<ExporterProfile>({
    queryKey: ['exporter_profile'],
    queryFn: () => fetchApi<ExporterProfile>('/api/v1/exporters/profile'),
  });
}

export function useReadinessGaps() {
  return useQuery<ReadinessGapAnalysis>({
    queryKey: ['exporter_readiness_gaps'],
    queryFn: () => fetchApi<ReadinessGapAnalysis>('/api/v1/exporters/readiness-gaps'),
  });
}

export function useSubmitOnboardingStep() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ step, data }: { step: number; data: Record<string, any> }) =>
      fetchApi<ExporterProfile>('/api/v1/exporters/onboarding/step', {
        method: 'POST',
        body: JSON.stringify({ step, data }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['exporter_profile'] });
      queryClient.invalidateQueries({ queryKey: ['exporter_readiness_gaps'] });
      queryClient.invalidateQueries({ queryKey: ['capability'] });
    },
  });
}
