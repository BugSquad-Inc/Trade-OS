import { fetchApi } from './client';

export type OutreachMode = 'email' | 'whatsapp' | 'phone_script';
export type OutreachLanguage = 'de' | 'en';

export interface CompliancePackDoc {
  doc_id: string;
  title: string;
  document_type: string;
  issuer: string;
  verified_date: string;
  file_format: string;
}

export interface CompliancePackResponse {
  bundle_id: string;
  buyer_id: string;
  buyer_name: string;
  exporter_name: string;
  documents: CompliancePackDoc[];
  total_documents: number;
  generated_at: string;
  download_url: string;
}

export interface OutreachResponse {
  action_id: string;
  buyer_id: string;
  buyer_name: string;
  contact_name: string;
  contact_title: string;
  mode: OutreachMode;
  language: OutreachLanguage;
  tone: string;
  subject: string;
  body: string;
  why_matches_you: string[];
  compliance_pack_docs: string[];
  status: string;
}

export const generateOutreachApi = (payload: {
  buyer_id: string;
  mode?: OutreachMode;
  language?: OutreachLanguage;
  tone?: string;
  contact_name?: string;
}) =>
  fetchApi<OutreachResponse>('/api/v1/outreach', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

export const getCompliancePackApi = (buyerId: string) =>
  fetchApi<CompliancePackResponse>(`/api/v1/outreach/compliance-pack/${buyerId}`);
