import React from 'react';
import { Search, Command, ShieldCheck, Activity } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const GlassTopbar: React.FC = () => {
  const { currentView, setCommandBarOpen } = useUIStore();

  const titles: Record<string, string> = {
    matches: "Screen 1: Match Portal (European Buyer Matches)",
    signals: "Screen 2: Live Trade Signals & EUDR 68/100 Readiness",
    accounts: "Screen 3: Account 360 Dossier & LangGraph Agents",
    customs: "Screen 4: Customs Bill of Lading (BOL) Manifest Intelligence",
  };

  return (
    <header className="h-16 glass-topbar flex items-center justify-between px-6 select-none shrink-0">
      <div>
        <h2 className="text-sm font-semibold text-white tracking-tight">{titles[currentView]}</h2>
        <p className="text-xs text-zinc-400">Leather & Materials Export Intelligence Engine</p>
      </div>

      <div className="flex items-center gap-3">
        {/* Spotlight Command Bar Trigger */}
        <button
          type="button"
          onClick={() => setCommandBarOpen(true)}
          className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-zinc-900/80 border border-white/[0.08] text-xs text-zinc-400 hover:text-zinc-200 hover:border-white/[0.15] transition-all cursor-pointer shadow-sm"
        >
          <Search size={14} />
          <span>Spotlight Search...</span>
          <kbd className="flex items-center gap-0.5 text-[10px] font-mono px-1.5 py-0.5 bg-zinc-800 text-zinc-300 rounded border border-white/[0.06]">
            <Command size={10} /> K
          </kbd>
        </button>

        {/* Live Status Pill */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-medium">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>Live Medallion Sync</span>
        </div>
      </div>
    </header>
  );
};
