import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export interface ProductCertificate {
  id: string;
  product_version_id: string;
  cert_type: string;
  certificate_name: string;
  issuer: string;
  accredited_lab?: string;
  scope?: string;
  file_hash?: string;
  issue_date: string;
  expiry_date?: string;
  status: string;
  verified_by?: string;
  verified_at?: string;
  created_at: string;
}

export interface ProductPassport {
  id: string;
  product_version_id: string;
  passport_number: string;
  status: string;
  recipient_buyer_id?: string;
  generated_at: string;
  passport_metadata: Record<string, any>;
}

export interface ProductVersion {
  id: string;
  product_family_id: string;
  version_tag: string;
  materials: string[];
  finishes: string[];
  thickness_range_mm: string[];
  monthly_capacity_sqft: number;
  moq_sqft: number;
  lead_time_days: number;
  sample_lead_time_days: number;
  price_basis_inr: number;
  price_basis_usd: number;
  incoterms: string[];
  status: string;
  approved_by?: string;
  approved_at?: string;
  created_at: string;
  certificates: ProductCertificate[];
  passports: ProductPassport[];
}

export interface ProductFamily {
  id: string;
  tenant_id?: string;
  name: string;
  category: string;
  hs_code: string;
  itc_hs_code?: string;
  leather_type: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  versions: ProductVersion[];
}

export function useProducts() {
  return useQuery<ProductFamily[]>({
    queryKey: ['products'],
    queryFn: () => fetchApi<ProductFamily[]>('/api/v1/products'),
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<ProductFamily>) =>
      fetchApi<ProductFamily>('/api/v1/products', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}
