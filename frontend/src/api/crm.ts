import { fetchApi } from './client';

export interface CRMExportResponse {
  export_id: string;
  buyer_id: string;
  buyer_name: string;
  format: string;
  status: string;
  payload: Record<string, any>;
  download_url?: string;
  message: string;
}

export const exportCRM = (buyerId: string, format: 'hubspot' | 'salesforce' | 'csv') =>
  fetchApi<CRMExportResponse>('/api/v1/crm/export', {
    method: 'POST',
    body: JSON.stringify({ buyer_id: buyerId, export_format: format }),
  });
