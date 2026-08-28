import { fetchApi } from './client';
import { DriverItem } from './matches';

export interface ContactDetail {
  id: string;
  full_name: string;
  title?: string;
  email?: string;
  phone?: string;
  linkedin_url?: string;
  is_primary: boolean;
  confidence: number;
  verification_status: string;
  consent_status: string;
  legal_basis: string;
}

export interface ProductDetail {
  id: string;
  name: string;
  description?: string;
  hs_code?: string;
  material_types: string[];
  tannage: string[];
  thickness_range_mm: string[];
  finish: string[];
}

export interface Account360 {
  id: string;
  canonical_name: string;
  legal_name?: string;
  domain?: string;
  country_code: string;
  country: string;
  city?: string;
  region?: string;
  website?: string;
  linkedin_url?: string;
  segment: string;
  description?: string;
  founded_year?: number;
  employee_range?: string;
  status: string;
  match_score?: number;
  grade?: string;
  rank?: number;
  drivers: DriverItem[];
  key_gaps: string[];
  next_best_action?: string;
  outreach_angle?: string;
  contacts: ContactDetail[];
  products: ProductDetail[];
  certifications: any[];
  signals: any[];
  eudr_requirements: any[];
  lane_economics: Record<string, any>;
}

export const getAccount360 = (id: string) => fetchApi<Account360>(`/api/v1/accounts/${id}`);

export const generateOutreachApi = (payload: { buyer_id: string; tone: string; contact_name?: string }) =>
  fetchApi<{
    action_id: string;
    buyer_id: string;
    buyer_name: string;
    contact_name: string;
    contact_title: string;
    tone: string;
    subject: string;
    body: string;
    status: string;
  }>('/api/v1/outreach', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
