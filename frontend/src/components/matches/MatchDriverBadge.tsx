import React from 'react';
import { CheckCircle2 } from 'lucide-react';
import { DriverItem } from '../../api/matches';

interface Props {
  driver: DriverItem;
}

export const MatchDriverBadge: React.FC<Props> = ({ driver }) => {
  return (
    <div className="group relative">
      <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100/90 border border-slate-200/90 text-xs hover:border-blue-400 hover:bg-white transition-all cursor-help shadow-2xs">
        <CheckCircle2 size={13} className="text-emerald-600 shrink-0" />
        <span className="text-slate-700 font-medium">{driver.category}:</span>
        <span className="font-mono text-slate-900 font-bold">{driver.score}/{driver.weight}</span>
      </div>

      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-3 bg-white border border-slate-200/90 rounded-xl shadow-xl text-[11px] text-slate-700 opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-30">
        <p className="font-bold text-slate-900 mb-0.5">{driver.title}</p>
        <p className="text-slate-500 leading-relaxed">{driver.evidence}</p>
      </div>
    </div>
  );
};
