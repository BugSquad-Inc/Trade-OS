import React, { useEffect, useState } from 'react';
import { Ship, ArrowRight } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { PageSkeleton } from '../ui/PageSkeleton';
import { getCustomsShipmentsApi, CustomsShipmentItem } from '../../api/customs';

export const CustomsExplorerView: React.FC = () => {
  const [shipments, setShipments] = useState<CustomsShipmentItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getCustomsShipmentsApi(50)
      .then(res => setShipments(res.shipments))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <PageSkeleton />;

  const totalTEU = shipments.reduce((acc, s) => acc + s.teu_count, 0);
  const totalValue = shipments.reduce((acc, s) => acc + (s.declared_value_usd || 0), 0);

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-white via-slate-50 to-blue-50/40 border border-slate-200/90 shadow-sm backdrop-blur-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-blue-50 text-blue-600 border border-blue-200/80 shadow-2xs">
                <Ship size={18} />
              </span>
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Ocean Shipment Radar & Competitor Displacement</h2>
            </div>
            <p className="text-xs text-slate-500 max-w-2xl font-medium">
              Real-time ocean manifest records connecting Indian export ports (Chennai, Tuticorin, Kolkata) to European buyers (Hamburg, Genoa, Le Havre). Identify which overseas competitors you can displace.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2.5 bg-white border border-slate-200/90 rounded-2xl text-center shadow-2xs">
              <div className="text-[10px] uppercase font-bold text-slate-400">Tracked Containers</div>
              <div className="text-base font-bold text-slate-900 font-mono">{totalTEU} FEU</div>
            </div>
            <div className="px-4 py-2.5 bg-white border border-slate-200/90 rounded-2xl text-center shadow-2xs">
              <div className="text-[10px] uppercase font-bold text-slate-400">Verified Manifest Value</div>
              <div className="text-base font-bold text-emerald-600 font-mono">${(totalValue / 1000).toFixed(0)}k USD</div>
            </div>
          </div>
        </div>
      </div>

      {/* Shipment Manifest Stream */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
          <span>Recent Ocean Manifests ({shipments.length})</span>
          <span>Verified Port Customs Clearance</span>
        </div>

        {shipments.map((s) => (
          <AppleCard key={s.id} variant="default" className="p-4 hover:border-blue-400/40 hover:shadow-md transition-all bg-white">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono text-xs font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                    {s.bol_number}
                  </span>
                  <h4 className="text-sm font-bold text-slate-900">{s.importer_name}</h4>
                  <AppleBadge tone="blue" size="sm">HS {s.hs_code}</AppleBadge>
                </div>
                <p className="text-xs text-slate-600">{s.product_desc}</p>
                <div className="flex items-center gap-4 text-[11px] text-slate-400 flex-wrap">
                  <span>Current Shipper: <b className="text-rose-700 bg-rose-50 px-1.5 py-0.5 rounded border border-rose-200">{s.exporter_name}</b></span>
                  <span>Weight: <b className="text-slate-700 font-mono">{s.weight_kg.toLocaleString()} kg</b></span>
                  <span>Date: <b className="text-slate-700 font-mono">{s.shipment_date}</b></span>
                  <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full font-semibold border border-emerald-200">
                    ⚡ Displacement Opportunity (Faster Chennai Transit)
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-4 border-t md:border-t-0 md:border-l border-slate-100 pt-3 md:pt-0 md:pl-6">
                <div className="flex items-center gap-2 text-xs font-mono">
                  <span className="px-2.5 py-1 bg-slate-100 text-slate-800 font-semibold rounded-lg border border-slate-200">{s.origin_port}</span>
                  <ArrowRight size={13} className="text-slate-400" />
                  <span className="px-2.5 py-1 bg-slate-100 text-slate-800 font-semibold rounded-lg border border-slate-200">{s.destination_port}</span>
                </div>
                {s.declared_value_usd && (
                  <div className="text-right font-mono text-xs text-emerald-600 font-bold">
                    ${s.declared_value_usd.toLocaleString()}
                  </div>
                )}
              </div>
            </div>
          </AppleCard>
        ))}
      </div>
    </div>
  );
};
