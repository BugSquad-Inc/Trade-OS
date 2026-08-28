import { fetchApi } from './client';

export interface CustomsShipmentItem {
  id: string;
  bol_number: string;
  shipment_date: string;
  importer_name: string;
  exporter_name: string;
  origin_port: string;
  destination_port: string;
  hs_code: string;
  product_desc: string;
  weight_kg: number;
  teu_count: number;
  declared_value_usd?: number;
}

export interface CustomsShipmentsListResponse {
  total_count: number;
  shipments: CustomsShipmentItem[];
}

export const getCustomsShipmentsApi = (limit: number = 50) =>
  fetchApi<CustomsShipmentsListResponse>(`/api/v1/customs/shipments?limit=${limit}`);
