import React from 'react';
import { Ship, Plane, Anchor, CheckCircle2, ArrowRight, DollarSign, Clock, MapPin } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useShipments, useUpdateShipmentMilestone, ShipmentRecord, ShipmentMilestone } from '../../api/shipments';

export const ShipmentMilestoneTrackerView: React.FC = () => {
  const { data: shipments, isLoading } = useShipments();
  const updateMilestone = useUpdateShipmentMilestone();

  if (isLoading) return <PageSkeleton />;

  const shipmentList = shipments || [];

  const milestones: { key: ShipmentMilestone; label: string }[] = [
    { key: 'booking_confirmed', label: 'Booking' },
    { key: 'cargo_picked', label: 'Picked' },
    { key: 'customs_cleared_origin', label: 'Origin Customs' },
    { key: 'vessel_departed', label: 'Departed' },
    { key: 'vessel_arrived', label: 'Arrived Port' },
    { key: 'customs_cleared_dest', label: 'EU Customs Cleared' },
    { key: 'delivered', label: 'Delivered' },
  ];

  const handleAdvance = (shipment: ShipmentRecord) => {
    const sequence: Record<ShipmentMilestone, ShipmentMilestone> = {
      booking_confirmed: 'cargo_picked',
      cargo_picked: 'customs_cleared_origin',
      customs_cleared_origin: 'vessel_departed',
      vessel_departed: 'vessel_arrived',
      transshipment: 'vessel_arrived',
      vessel_arrived: 'customs_cleared_dest',
      customs_cleared_dest: 'delivered',
      delivered: 'delivered',
    };
    const next = sequence[shipment.milestone] || 'delivered';
    updateMilestone.mutate({
      shipmentId: shipment.id,
      milestone: next,
      ebrc_status: next === 'delivered' ? 'realized' : shipment.ebrc_status,
      realized_amount_inr: next === 'delivered' ? shipment.invoice_amount_usd * 92.5 : shipment.realized_amount_inr,
    });
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-900 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold tracking-tight">Active Ocean & Air Shipments + DGFT eBRC Radar</h2>
            <span className="px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-200 text-[11px] font-medium border border-blue-400/20">
              Live Container Tracking
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-xl font-medium">
            Real-time port dispatch milestones, vessel coordinates, European customs clearance, and bank foreign remittance realization.
          </p>
        </div>
      </div>

      {/* Shipment Cards */}
      {shipmentList.length === 0 ? (
        <EmptyState title="No Active Shipments" description="Create a shipment booking from an approved purchase order." />
      ) : (
        <div className="space-y-5">
          {shipmentList.map((shp) => {
            const isAir = shp.carrier.toLowerCase().includes('lufthansa') || shp.container_number.includes('LH');
            const currentIndex = milestones.findIndex((m) => m.key === shp.milestone);

            return (
              <AppleCard
                key={shp.id}
                variant="default"
                className="bg-white border-slate-200/90 shadow-2xs hover:border-blue-300 transition-all p-5 space-y-4"
              >
                {/* Top Row: Details & Values */}
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      {isAir ? <Plane size={18} className="text-blue-600" /> : <Ship size={18} className="text-blue-600" />}
                      <h4 className="text-base font-bold text-slate-900">{shp.vessel_name}</h4>
                      <AppleBadge tone="blue" size="sm">Voyage: {shp.voyage_number}</AppleBadge>
                      <AppleBadge tone={shp.tracking_status === 'on_time' ? 'green' : 'red'} size="sm">
                        {shp.tracking_status.replace('_', ' ').toUpperCase()}
                      </AppleBadge>
                    </div>
                    <p className="text-xs text-slate-500 font-mono">
                      Container / AWB: <b className="text-slate-800">{shp.container_number}</b> · Carrier: {shp.carrier} · Ref: {shp.shipment_ref}
                    </p>
                  </div>

                  <div className="flex items-center gap-4 shrink-0 text-left md:text-right">
                    <div>
                      <p className="text-[10px] uppercase font-bold text-slate-400">Invoice Amount</p>
                      <p className="text-sm font-bold font-mono text-slate-900">${shp.invoice_amount_usd.toLocaleString()}</p>
                    </div>
                    <div className="border-l border-slate-200 pl-4">
                      <p className="text-[10px] uppercase font-bold text-slate-400">DGFT eBRC Bank Realization</p>
                      <span
                        className={`text-xs font-bold font-mono px-2 py-0.5 rounded-md ${
                          shp.ebrc_status === 'realized'
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}
                      >
                        {shp.ebrc_status === 'realized' ? `Realized (₹${(shp.realized_amount_inr / 100000).toFixed(2)}L)` : 'Pending B/L Copy'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Ports & Dates */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs bg-slate-50/70 p-3.5 rounded-2xl border border-slate-100">
                  <div className="flex items-center gap-2">
                    <MapPin size={14} className="text-slate-400" />
                    <div>
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Origin Port</span>
                      <p className="font-semibold text-slate-800">{shp.origin_port} (ETD: {shp.etd})</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin size={14} className="text-blue-500" />
                    <div>
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Destination Port</span>
                      <p className="font-semibold text-slate-800">{shp.destination_port} (ETA: {shp.eta})</p>
                    </div>
                  </div>
                </div>

                {/* Milestone Stepper */}
                <div className="space-y-2 pt-1">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Milestone Progression</span>
                  <div className="grid grid-cols-2 sm:grid-cols-7 gap-2">
                    {milestones.map((m, idx) => {
                      const isDone = idx <= currentIndex;
                      const isCurrent = idx === currentIndex;
                      return (
                        <div
                          key={m.key}
                          className={`p-2 rounded-xl text-center border text-[10px] font-semibold transition-all ${
                            isCurrent
                              ? 'bg-blue-600 text-white border-blue-600 shadow-xs'
                              : isDone
                              ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                              : 'bg-slate-50 text-slate-400 border-slate-200'
                          }`}
                        >
                          {m.label}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Bottom Action */}
                <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                  <span className="text-xs text-slate-500 font-medium">
                    Gross Weight: <b className="text-slate-800">{shp.gross_weight_kg.toLocaleString()} kg</b>
                  </span>

                  {shp.milestone !== 'delivered' && (
                    <AppleButton
                      variant="primary"
                      size="sm"
                      icon={<ArrowRight size={13} />}
                      onClick={() => handleAdvance(shp)}
                    >
                      Advance Milestone
                    </AppleButton>
                  )}
                </div>
              </AppleCard>
            );
          })}
        </div>
      )}
    </div>
  );
};
