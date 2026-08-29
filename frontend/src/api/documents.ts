import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export type DocumentType =
  | 'eudr_dds'
  | 'lab_test_report'
  | 'commercial_invoice'
  | 'packing_list'
  | 'bill_of_lading'
  | 'certificate_of_origin'
  | 'rcmc_cle'
  | 'ebrc_certificate';

export interface TradeDocument {
  id: string;
  tenant_id?: string;
  opportunity_id?: string;
  shipment_id?: string;
  product_version_id?: string;
  doc_type: DocumentType;
  title: string;
  file_name: string;
  file_size_bytes: number;
  file_hash_sha256: string;
  mime_type: string;
  storage_uri: string;
  status: string;
  metadata_json: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ComplianceCheckItem {
  regulation: string;
  requirement: string;
  passed: boolean;
  weight: number;
  evidence: string;
}

export interface ComplianceAuditResponse {
  overall_score: number;
  clearance_grade: string;
  status: string;
  checks: ComplianceCheckItem[];
  remediation_actions: string[];
  audited_at: string;
  auditor: string;
}

export function useDocuments(docType?: string, opportunityId?: string) {
  const params = new URLSearchParams();
  if (docType) params.append('doc_type', docType);
  if (opportunityId) params.append('opportunity_id', opportunityId);
  const queryStr = params.toString() ? `?${params.toString()}` : '';

  return useQuery<TradeDocument[]>({
    queryKey: ['documents', docType, opportunityId],
    queryFn: () => fetchApi<TradeDocument[]>(`/api/v1/documents${queryStr}`),
  });
}

export function useComplianceAudit() {
  return useMutation({
    mutationFn: (data: {
      exporter_certs?: string[];
      has_farm_polygons?: boolean;
      cr_vi_tested_zero?: boolean;
      reach_svhc_zero?: boolean;
    }) =>
      fetchApi<ComplianceAuditResponse>('/api/v1/documents/compliance-audit', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
  });
}

export function useUploadDocument() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<TradeDocument>) =>
      fetchApi<TradeDocument>('/api/v1/documents', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['documents'] });
    },
  });
}
