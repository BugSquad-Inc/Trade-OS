import React from 'react';
import { Search, Command } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const GlassTopbar: React.FC = () => {
  const { currentView, setCommandBarOpen } = useUIStore();

  const titles: Record<string, string> = {
    matches: "Screen 1: Qualified Buyer Match Portal (50+ European Importers)",
    signals: "Screen 2: Live European Market Signals & EUDR Compliance Radar",
    accounts: "Screen 3: Buyer Intelligence Dossier & AI Export Director",
    customs: "Screen 4: Ocean Shipment Radar & Competitor Displacement",
    analytics: "Screen 5: Executive Export Revenue & Pipeline Cockpit",
  };

  return (
    <header className="h-16 glass-topbar flex items-center justify-between px-6 select-none shrink-0 shadow-[0_1px_8px_rgba(0,0,0,0.02)]">
      <div className="flex items-center gap-4">
        <div>
          <h2 className="text-sm font-bold text-slate-900 tracking-tight">{titles[currentView]}</h2>
          <p className="text-xs text-slate-500 font-medium">Indian Leather & Finished Materials Export Revenue Engine</p>
        </div>

        {/* Demo Watermark Banner */}
        <div className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-800 text-[11px] font-medium">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
          <span>Demo Environment — Synthetic benchmark records for pilot validation</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Spotlight Command Bar Trigger */}
        <button
          type="button"
          onClick={() => setCommandBarOpen(true)}
          className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white border border-slate-200/90 text-xs text-slate-600 hover:text-slate-900 hover:border-slate-300 transition-all cursor-pointer shadow-xs"
        >
          <Search size={14} className="text-slate-400" />
          <span>Instant Buyer & HS Code Matcher...</span>
          <kbd className="flex items-center gap-0.5 text-[10px] font-mono px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded border border-slate-200">
            <Command size={10} /> K
          </kbd>
        </button>

        {/* Status Pill */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-100 border border-slate-200/80 text-slate-700 text-xs font-semibold shadow-xs">
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          <span>Market Feed: Verified Daily</span>
        </div>
      </div>
    </header>
  );
};
