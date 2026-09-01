import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export interface ProductSpecification {
  id?: string;
  thickness_min_mm: number;
  thickness_max_mm: number;
  temper: string;
  tensile_strength_n_per_mm2: number;
  tear_strength_n: number;
  grain_type: string;
  tannage_type: string;
  origin_country: string;
}

export interface ChemicalComplianceSpec {
  id?: string;
  chromium_vi_ppm: number;
  azo_dyes_ppm: number;
  formaldehyde_ppm: number;
  pfas_free: boolean;
  reach_svhc_status: string;
  lab_test_report_id?: string;
  accredited_lab: string;
  test_date?: string;
}

export interface TraceabilitySpec {
  id?: string;
  abattoir_license_no: string;
  mandal_district: string;
  state: string;
  geolocation_lat: number;
  geolocation_lng: number;
  eudr_cutoff_cleared: boolean;
  hide_origin_batch: string;
}

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
  public_token: string;
  qr_code_url?: string;
  carbon_footprint_kg_co2e: number;
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
  specifications?: ProductSpecification;
  chemical_spec?: ChemicalComplianceSpec;
  traceability_spec?: TraceabilitySpec;
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

export function usePublicDpp(publicToken?: string) {
  return useQuery<ProductPassport>({
    queryKey: ['publicDpp', publicToken],
    queryFn: () => fetchApi<ProductPassport>(`/api/v1/products/dpp/public/${publicToken}`),
    enabled: !!publicToken,
  });
}

export function useCreateProduct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: any) =>
      fetchApi<ProductFamily>('/api/v1/products', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}
