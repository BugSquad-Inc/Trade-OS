import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from './client';

export type ShipmentMilestone =
  | 'booking_confirmed'
  | 'cargo_picked'
  | 'customs_cleared_origin'
  | 'vessel_departed'
  | 'transshipment'
  | 'vessel_arrived'
  | 'customs_cleared_dest'
  | 'delivered';

export interface ShipmentRecord {
  id: string;
  tenant_id?: string;
  opportunity_id?: string;
  buyer_id: string;
  shipment_ref: string;
  container_number: string;
  vessel_name: string;
  voyage_number: string;
  carrier: string;
  origin_port: string;
  destination_port: string;
  etd: string;
  eta: string;
  milestone: ShipmentMilestone;
  tracking_status: 'on_time' | 'delayed' | 'customs_hold';
  gross_weight_kg: number;
  invoice_amount_usd: number;
  realized_amount_inr: number;
  ebrc_status: 'pending' | 'applied' | 'realized' | 'closed';
  ebrc_number?: string;
  created_at: string;
  updated_at: string;
  buyer?: {
    canonical_name: string;
  };
}

export function useShipments() {
  return useQuery<ShipmentRecord[]>({
    queryKey: ['shipments'],
    queryFn: () => fetchApi<ShipmentRecord[]>('/api/v1/shipments'),
  });
}

export function useUpdateShipmentMilestone() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      shipmentId,
      milestone,
      tracking_status,
      ebrc_status,
      realized_amount_inr,
    }: {
      shipmentId: string;
      milestone: ShipmentMilestone;
      tracking_status?: string;
      ebrc_status?: string;
      realized_amount_inr?: number;
    }) =>
      fetchApi<ShipmentRecord>(`/api/v1/shipments/${shipmentId}/milestone`, {
        method: 'PATCH',
        body: JSON.stringify({
          milestone,
          tracking_status,
          ebrc_status,
          realized_amount_inr,
        }),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shipments'] });
    },
  });
}
