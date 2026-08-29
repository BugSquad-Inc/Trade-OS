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
    <AppleCard variant="default" className="relative overflow-hidden border-slate-200/90 bg-gradient-to-r from-white via-slate-50/90 to-blue-50/30 shadow-sm">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-50 text-blue-600 border border-blue-200/80 shadow-2xs">
              <Factory size={22} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-slate-900 tracking-tight">{capability.company_name}</h2>
                <AppleBadge tone="blue" size="sm">Design Partner #1</AppleBadge>
                <AppleBadge tone="green" size="sm" dot>EUDR Ready</AppleBadge>
              </div>
              <p className="text-xs text-slate-500 font-medium flex items-center gap-1.5 mt-0.5">
                <MapPin size={13} className="text-slate-400" />
                <span>{capability.location}</span> · <span>{capability.cluster}</span>
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 text-xs">
            <span className="px-2.5 py-1 rounded-lg bg-white text-slate-700 border border-slate-200/90 shadow-2xs">
              🏭 Capacity: <b className="text-slate-900 font-mono">{capability.monthly_capacity_sqft.toLocaleString()} sqft/mo</b>
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-white text-slate-700 border border-slate-200/90 shadow-2xs">
              📦 MOQ: <b className="text-slate-900 font-mono">{capability.moq_sqft.toLocaleString()} sqft</b>
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-white text-slate-700 border border-slate-200/90 shadow-2xs">
              ⏱ Lead Time: <b className="text-slate-900 font-mono">{capability.lead_time_days} days</b> (Air Sample: {capability.sample_lead_time_days}d)
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-white text-slate-700 border border-slate-200/90 shadow-2xs">
              🚢 Port: <b className="text-slate-900">{capability.port_of_export}</b>
            </span>
          </div>
        </div>

        <div className="w-full md:w-auto flex items-center justify-between md:justify-end gap-4 p-4 rounded-2xl bg-white border border-slate-200/90 shadow-sm shrink-0">
          <div className="text-left md:text-right">
            <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">EU & UK Market Readiness</p>
            <p className="text-2xl font-bold font-mono text-emerald-600">{capability.eudr_readiness_score}<span className="text-sm text-slate-400">/100</span></p>
            <p className="text-[10px] text-slate-500 font-medium">LWG & Traceability Ready</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-50 border border-emerald-200/80 flex items-center justify-center text-emerald-600 shadow-2xs">
            <ShieldCheck size={26} />
          </div>
        </div>
      </div>
    </AppleCard>
  );
};
