import React from 'react';
import { Ship } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';

interface Props {
  benchmark?: {
    origin_port: string;
    destination_port: string;
    mode: string;
    container_type: string;
    rate_usd: number;
    rate_spread: string;
    transit_days: string;
    port_congestion_index: string;
    reroute_risk_notes?: string;
    sample_air_transit: string;
  };
}

export const FreightLaneWidget: React.FC<Props> = ({ benchmark }) => {
  if (!benchmark) return null;

  return (
    <AppleCard variant="default" className="space-y-4 border-teal-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-teal-500/10 text-teal-400 border border-teal-500/20">
            <Ship size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">Chennai → Hamburg Trade Corridor</h3>
            <p className="text-xs text-zinc-400">Ocean Freight & Landed Cost Economics</p>
          </div>
        </div>
        <AppleBadge tone="teal" size="sm">Active Benchmark</AppleBadge>
      </div>

      <div className="grid grid-cols-3 gap-3 text-center">
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05]">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase">Spot Rate (40HC)</p>
          <p className="text-lg font-bold font-mono text-teal-300 mt-0.5">${benchmark.rate_usd.toLocaleString()}</p>
          <p className="text-[10px] text-zinc-500">{benchmark.rate_spread}</p>
        </div>
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05]">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase">Ocean Transit</p>
          <p className="text-lg font-bold font-mono text-white mt-0.5">{benchmark.transit_days}</p>
          <p className="text-[10px] text-zinc-500">Port to Port</p>
        </div>
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05]">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase">Air Sample</p>
          <p className="text-lg font-bold font-mono text-blue-300 mt-0.5">{benchmark.sample_air_transit}</p>
          <p className="text-[10px] text-zinc-500">To Frankfurt (FRA)</p>
        </div>
      </div>
    </AppleCard>
  );
};
