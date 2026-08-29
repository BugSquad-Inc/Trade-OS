import React from 'react';
import { Search, Command, Menu } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';
import { SimpleModeToggle } from '../ui/SimpleModeToggle';

export const GlassTopbar: React.FC = () => {
  const { currentView, setCommandBarOpen, setMobileDrawerOpen } = useUIStore();

  const titles: Record<string, string> = {
    today: "Today Priority Action Cockpit",
    deals: "12-Stage Export Deals & Quotation Pipeline",
    matches: "Buyer Match Portal (50+ European Importers)",
    signals: "Live European Market Signals & Compliance Radar",
    accounts: "Buyer Intelligence Dossier & AI Sales Action",
    products: "Digital Product Passports & EU Compliance Spec",
    customs: "Ocean Shipment Radar & Displacement",
    analytics: "Revenue & KPI Cockpit",
    verification: "Analyst Verification & Entity Resolution Queue",
  };

  return (
    <header className="h-16 glass-topbar flex items-center justify-between px-4 sm:px-6 select-none shrink-0 shadow-[0_1px_8px_rgba(0,0,0,0.02)] gap-3">
      <div className="flex items-center gap-3 min-w-0">
        {/* Mobile Menu Button */}
        <button
          type="button"
          onClick={() => setMobileDrawerOpen(true)}
          className="lg:hidden p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200/80 shrink-0"
          aria-label="Open Navigation Menu"
        >
          <Menu size={18} />
        </button>

        <div className="min-w-0">
          <h2 className="text-sm font-bold text-slate-900 tracking-tight truncate">{titles[currentView]}</h2>
          <p className="text-xs text-slate-500 font-medium hidden sm:block">Indian Leather & Materials Export Revenue OS</p>
        </div>

        {/* Demo Watermark Banner */}
        <div className="hidden xl:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-800 text-[11px] font-medium shrink-0">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
          <span>Demo Environment — Synthetic Sample Data</span>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-3 shrink-0">
        {/* Simple Mode Toggle */}
        <SimpleModeToggle />

        {/* Team Management & RBAC Button */}
        <button
          type="button"
          onClick={() => useUIStore.getState().setTeamModalOpen(true)}
          className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-white border border-slate-200/90 text-xs text-slate-700 hover:text-slate-900 hover:border-slate-300 transition-all cursor-pointer shadow-xs"
        >
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          <span className="font-bold hidden md:inline">Butler's Org</span>
          <span className="text-[10px] font-mono px-1 py-0.2 rounded bg-purple-100 text-purple-700 font-bold">Owner</span>
        </button>

        {/* Spotlight Command Bar Trigger */}
        <button
          type="button"
          onClick={() => setCommandBarOpen(true)}
          className="flex items-center gap-2 px-2.5 sm:px-3 py-1.5 rounded-xl bg-white border border-slate-200/90 text-xs text-slate-600 hover:text-slate-900 hover:border-slate-300 transition-all cursor-pointer shadow-xs"
        >
          <Search size={14} className="text-slate-400" />
          <span className="hidden sm:inline">Buyer & HS Code Matcher...</span>
          <kbd className="flex items-center gap-0.5 text-[10px] font-mono px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded border border-slate-200">
            <Command size={10} /> K
          </kbd>
        </button>
      </div>
    </header>
  );
};
