import { fetchApi } from './client';

export interface ExporterCapability {
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
}

export const getCapability = () => fetchApi<ExporterCapability>('/api/v1/capability');
