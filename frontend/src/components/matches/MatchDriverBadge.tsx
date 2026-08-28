import React from 'react';
import { CheckCircle2 } from 'lucide-react';
import { DriverItem } from '../../api/matches';

interface Props {
  driver: DriverItem;
}

export const MatchDriverBadge: React.FC<Props> = ({ driver }) => {
  return (
    <div className="group relative">
      <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-800/70 border border-white/[0.06] text-xs hover:border-blue-500/40 transition-colors cursor-help">
        <CheckCircle2 size={13} className="text-emerald-400 shrink-0" />
        <span className="text-zinc-300 font-medium">{driver.category}:</span>
        <span className="font-mono text-white font-semibold">{driver.score}/{driver.weight}</span>
      </div>

      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-2.5 bg-zinc-900 border border-white/[0.12] rounded-xl shadow-2xl text-[11px] text-zinc-300 opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-30">
        <p className="font-semibold text-white mb-0.5">{driver.title}</p>
        <p className="text-zinc-400">{driver.evidence}</p>
      </div>
    </div>
  );
};
