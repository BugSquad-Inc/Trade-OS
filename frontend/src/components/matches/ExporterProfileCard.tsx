import React from 'react';
import { Factory, ShieldCheck, MapPin } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { ExporterCapability } from '../../api/capability';

interface Props {
  capability?: ExporterCapability;
}

export const ExporterProfileCard: React.FC<Props> = ({ capability }) => {
  if (!capability) return null;

  return (
    <AppleCard variant="default" className="relative overflow-hidden border-blue-500/20 bg-gradient-to-r from-zinc-900/90 via-zinc-900/80 to-blue-950/20">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Factory size={22} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-white tracking-tight">{capability.company_name}</h2>
                <AppleBadge tone="blue" size="sm">Design Partner #1</AppleBadge>
                <AppleBadge tone="green" size="sm" dot>EUDR Ready</AppleBadge>
              </div>
              <p className="text-xs text-zinc-400 flex items-center gap-1.5 mt-0.5">
                <MapPin size={13} className="text-zinc-500" />
                <span>{capability.location}</span> · <span>{capability.cluster}</span>
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 text-xs">
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              🏭 Capacity: <b className="text-white font-mono">{capability.monthly_capacity_sqft.toLocaleString()} sqft/mo</b>
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              📦 MOQ: <b className="text-white font-mono">{capability.moq_sqft.toLocaleString()} sqft</b>
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              ⏱ Lead Time: <b className="text-white font-mono">{capability.lead_time_days} days</b> (Air Sample: {capability.sample_lead_time_days}d)
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              🚢 Port: <b className="text-white">{capability.port_of_export}</b>
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4 p-4 rounded-xl bg-zinc-950/60 border border-white/[0.08] shrink-0">
          <div className="text-right">
            <p className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">EUDR Readiness</p>
            <p className="text-2xl font-bold font-mono text-emerald-400">{capability.eudr_readiness_score}<span className="text-sm text-zinc-500">/100</span></p>
            <p className="text-[10px] text-zinc-400">Due Diligence Ready</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <ShieldCheck size={26} />
          </div>
        </div>
      </div>
    </AppleCard>
  );
};
