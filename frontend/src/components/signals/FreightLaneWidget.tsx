import React, { useState } from 'react';
import { Ship } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';

interface Props {
  benchmark?: any;
}

const CORRIDORS = [
  { id: 'DEHAM', label: 'Chennai ➔ Hamburg 🇩🇪', origin: 'INMAA', dest: 'DEHAM', rate: 1850, transit: '26–34 days', cost_eur_sqft: '€0.42/sqft', congestion: 'Normal' },
  { id: 'ITGOA', label: 'Chennai ➔ Genoa 🇮🇹', origin: 'INMAA', dest: 'ITGOA', rate: 1720, transit: '22–28 days', cost_eur_sqft: '€0.39/sqft', congestion: 'Low' },
  { id: 'FRLEH', label: 'Kolkata ➔ Le Havre 🇫🇷', origin: 'INCCU', dest: 'FRLEH', rate: 2100, transit: '28–36 days', cost_eur_sqft: '€0.48/sqft', congestion: 'Moderate' },
  { id: 'ESVLC', label: 'Tuticorin ➔ Valencia 🇪🇸', origin: 'INTUT', dest: 'ESVLC', rate: 1650, transit: '20–26 days', cost_eur_sqft: '€0.37/sqft', congestion: 'Optimal' },
];

export const FreightLaneWidget: React.FC<Props> = ({ benchmark }) => {
  const [selectedCorridor, setSelectedCorridor] = useState('DEHAM');
  const active = CORRIDORS.find(c => c.id === selectedCorridor) || CORRIDORS[0];

  return (
    <AppleCard variant="default" className="space-y-4 border-teal-500/20 bg-white">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-teal-50 text-teal-700 border border-teal-200/80 shadow-2xs">
            <Ship size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 tracking-tight">Multi-Corridor Ocean Freight Matrix</h3>
            <p className="text-xs text-slate-500 font-medium">Landed Cost Economics & Port Transit Times</p>
          </div>
        </div>
        <AppleBadge tone="teal" size="sm">Live Corridor</AppleBadge>
      </div>

      <AppleSegmentedControl
        size="sm"
        value={selectedCorridor}
        onChange={setSelectedCorridor}
        options={CORRIDORS.map(c => ({ value: c.id, label: c.label }))}
      />

      <div className="grid grid-cols-3 gap-3 text-center">
        <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200/80 shadow-2xs">
          <p className="text-[10px] font-bold text-slate-500 uppercase">Ocean Freight (40HC FEU)</p>
          <p className="text-lg font-bold font-mono text-teal-700 mt-0.5">${active.rate.toLocaleString()}</p>
          <p className="text-[10px] text-slate-400 font-medium">{active.origin} ➔ {active.dest}</p>
        </div>
        <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200/80 shadow-2xs">
          <p className="text-[10px] font-bold text-slate-500 uppercase">Ocean Transit</p>
          <p className="text-lg font-bold font-mono text-slate-900 mt-0.5">{active.transit}</p>
          <p className="text-[10px] text-slate-400 font-medium">Congestion: {active.congestion}</p>
        </div>
        <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200/80 shadow-2xs">
          <p className="text-[10px] font-bold text-slate-500 uppercase">Est. Landed Cost</p>
          <p className="text-lg font-bold font-mono text-emerald-700 mt-0.5">{active.cost_eur_sqft}</p>
          <p className="text-[10px] text-slate-400 font-medium">CIF European Port</p>
        </div>
      </div>
    </AppleCard>
  );
};
