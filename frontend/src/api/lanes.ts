import { fetchApi } from './client';

export interface TradeCorridorItem {
  corridor_id: string;
  origin_port: string;
  origin_city: string;
  destination_port: string;
  destination_city: string;
  destination_country: string;
  transit_days_min: number;
  transit_days_max: number;
  ocean_freight_usd_feu: number;
  landed_cost_eur_sqft: number;
  port_congestion_index: string;
}

export interface TradeCorridorListResponse {
  total_corridors: number;
  corridors: TradeCorridorItem[];
}

export const getTradeCorridorsApi = () =>
  fetchApi<TradeCorridorListResponse>('/api/v1/lanes/corridors');
