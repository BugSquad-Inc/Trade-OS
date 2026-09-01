import React from 'react';
import { Search, Command, Menu, BookOpen, Sparkles, SlidersHorizontal } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const GlassTopbar: React.FC = () => {
  const { currentView, workspaceMode, toggleWorkspaceMode, setCommandBarOpen, setMobileDrawerOpen, openGlossary } = useUIStore();

  const titles: Record<string, string> = {
    today: "Today Priority Action Items",
    sales: "Sales Hub · Buyers, Signals & Quotations",
    orders: "Orders Hub · Pipeline, Manufacturing & Shipments",
    money: "Money Hub · Invoices, Bank Realization & eBRC",
    business: "My Business Hub · Profile, Specs & Team",
    // Backstage views
    deals: "12-Stage Export Deals & Quotation Pipeline",
    matches: "Buyer Match Portal (50+ European Importers)",
    signals: "Live European Market Signals & Compliance Radar",
    accounts: "Buyer Intelligence Dossier & AI Sales Action",
    products: "Digital Product Passports & EU Compliance Spec",
    documents: "Export Document Vault & Compliance Audit",
    shipments: "Active Ocean Shipments & Bank eBRC Radar",
    customs: "Ocean Displacements Radar",
    analytics: "Revenue & KPI Cockpit",
    verification: "Analyst Verification & Entity Resolution Queue",
    audit: "Centralized Compliance & Security Audit Trail",
  };

  return (
    <header className="h-16 glass-topbar flex items-center justify-between px-4 sm:px-6 select-none shrink-0 shadow-[0_1px_8px_rgba(0,0,0,0.02)] gap-3 bg-white/80 backdrop-blur-md border-b border-slate-200/80">
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
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-bold text-slate-900 tracking-tight truncate">
              {titles[currentView] || "Export Revenue OS"}
            </h2>
            <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full font-bold hidden sm:inline-flex ${
              workspaceMode === 'owner' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'
            }`}>
              {workspaceMode === 'owner' ? 'Owner View' : 'Expert View'}
            </span>
          </div>
          <p className="text-xs text-slate-500 font-medium hidden sm:block">Indian Leather & Materials Export Revenue Operating System</p>
        </div>

        {/* Demo Watermark Banner */}
        <div className="hidden xl:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-800 text-[11px] font-medium shrink-0">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
          <span>Demo Environment — Synthetic Sample Data</span>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-3 shrink-0">
        {/* Export Glossary Button */}
        <button
          type="button"
          onClick={() => openGlossary()}
          className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-100/90 text-slate-700 hover:text-blue-700 hover:bg-blue-50/80 transition-all text-xs font-semibold cursor-pointer border border-slate-200/60"
          title="Open Plain-English Export Glossary"
        >
          <BookOpen size={14} className="text-blue-600" />
          <span className="hidden md:inline">Glossary</span>
        </button>

        {/* Workspace Mode Switcher Button */}
        <button
          type="button"
          onClick={toggleWorkspaceMode}
          className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer border shadow-2xs ${
            workspaceMode === 'owner'
              ? 'bg-blue-50 text-blue-700 border-blue-200/80 hover:bg-blue-100/80'
              : 'bg-purple-50 text-purple-700 border-purple-200/80 hover:bg-purple-100/80'
          }`}
          title={`Click to switch to ${workspaceMode === 'owner' ? 'Expert Workspace' : 'Owner Workspace'}`}
        >
          {workspaceMode === 'owner' ? (
            <>
              <Sparkles size={13} className="text-blue-600" />
              <span className="hidden sm:inline">Owner Jobs</span>
            </>
          ) : (
            <>
              <SlidersHorizontal size={13} className="text-purple-600" />
              <span className="hidden sm:inline">Expert Mode</span>
            </>
          )}
        </button>

        {/* Team Management & RBAC Button */}
        <button
          type="button"
          onClick={() => useUIStore.getState().setTeamModalOpen(true)}
          className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-white border border-slate-200/90 text-xs text-slate-700 hover:text-slate-900 hover:border-slate-300 transition-all cursor-pointer shadow-2xs"
        >
          <span className="w-2 h-2 rounded-full bg-emerald-500" />
          <span className="font-bold hidden md:inline">Butler's Org</span>
          <span className="text-[10px] font-mono px-1 py-0.2 rounded bg-purple-100 text-purple-700 font-bold">Owner</span>
        </button>

        {/* Spotlight Command Bar Trigger */}
        <button
          type="button"
          onClick={() => setCommandBarOpen(true)}
          className="flex items-center gap-2 px-2.5 sm:px-3 py-1.5 rounded-xl bg-white border border-slate-200/90 text-xs text-slate-600 hover:text-slate-900 hover:border-slate-300 transition-all cursor-pointer shadow-2xs"
        >
          <Search size={14} className="text-slate-400" />
          <span className="hidden sm:inline">Search...</span>
          <kbd className="flex items-center gap-0.5 text-[10px] font-mono px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded border border-slate-200">
            <Command size={10} /> K
          </kbd>
        </button>
      </div>
    </header>
  );
};
