import React, { useEffect, useState } from 'react';
import { Anchor, Ship, FileText, ArrowRight, TrendingUp, DollarSign, Box } from 'lucide-react';
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
      <div className="p-6 rounded-3xl bg-gradient-to-r from-blue-950/40 via-zinc-900/80 to-zinc-900/40 border border-blue-500/20 backdrop-blur-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-blue-500/20 text-blue-400">
                <Ship size={18} />
              </span>
              <h2 className="text-xl font-bold text-white tracking-tight">Customs Bill of Lading (BOL) Manifest Flows</h2>
            </div>
            <p className="text-xs text-zinc-400 max-w-2xl">
              Real-time ocean manifest records connecting Indian export hubs (Chennai, Tuticorin, Kolkata) to European discharge ports (Hamburg, Genoa, Le Havre).
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2 bg-zinc-900/80 border border-white/[0.08] rounded-xl text-center">
              <div className="text-[10px] uppercase font-semibold text-zinc-500">Tracked Containers</div>
              <div className="text-base font-bold text-white font-mono">{totalTEU} FEU</div>
            </div>
            <div className="px-4 py-2 bg-zinc-900/80 border border-white/[0.08] rounded-xl text-center">
              <div className="text-[10px] uppercase font-semibold text-zinc-500">Verified Manifest Value</div>
              <div className="text-base font-bold text-emerald-400 font-mono">${(totalValue / 1000).toFixed(0)}k USD</div>
            </div>
          </div>
        </div>
      </div>

      {/* Shipment Manifest Stream */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs font-semibold text-zinc-400 uppercase tracking-wider px-1">
          <span>Recent Ocean Manifests ({shipments.length})</span>
          <span>Verified Port Customs Clearance</span>
        </div>

        {shipments.map((s) => (
          <AppleCard key={s.id} variant="default" className="p-4 hover:border-blue-500/40 transition-all">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono text-xs font-bold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                    {s.bol_number}
                  </span>
                  <h4 className="text-sm font-bold text-white">{s.importer_name}</h4>
                  <AppleBadge tone="blue" size="sm">HS {s.hs_code}</AppleBadge>
                </div>
                <p className="text-xs text-zinc-300">{s.product_desc}</p>
                <div className="flex items-center gap-4 text-[11px] text-zinc-500">
                  <span>Shipper: <b className="text-zinc-400">{s.exporter_name}</b></span>
                  <span>Weight: <b className="text-zinc-400">{s.weight_kg.toLocaleString()} kg</b></span>
                  <span>Date: <b className="text-zinc-400">{s.shipment_date}</b></span>
                </div>
              </div>

              <div className="flex items-center gap-4 border-t md:border-t-0 md:border-l border-white/[0.08] pt-3 md:pt-0 md:pl-6">
                <div className="flex items-center gap-2 text-xs font-mono">
                  <span className="px-2 py-1 bg-zinc-800 text-zinc-300 rounded">{s.origin_port}</span>
                  <ArrowRight size={13} className="text-zinc-500" />
                  <span className="px-2 py-1 bg-zinc-800 text-zinc-300 rounded">{s.destination_port}</span>
                </div>
                {s.declared_value_usd && (
                  <div className="text-right font-mono text-xs text-emerald-400 font-bold">
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
