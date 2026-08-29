import React from 'react';
import { LayoutGrid, Radio, Building2, Layers, Ship, BarChart3, X, CheckCircle, FileCheck, ShieldCheck } from 'lucide-react';
import { useUIStore, AppView } from '../../store/uiStore';

export const GlassSidebar: React.FC = () => {
  const { currentView, setCurrentView, isMobileDrawerOpen, setMobileDrawerOpen, setOnboardingModalOpen } = useUIStore();

  const navItems: { id: AppView; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'today', label: 'Today Action Cockpit', icon: <BarChart3 size={18} />, badge: 'Focus' },
    { id: 'deals', label: '12-Stage Export Pipeline', icon: <Layers size={18} />, badge: 'Deals' },
    { id: 'matches', label: 'Buyer Match Portal', icon: <LayoutGrid size={18} />, badge: '50+ Verified' },
    { id: 'signals', label: 'Live Market Signals', icon: <Radio size={18} />, badge: 'Live' },
    { id: 'accounts', label: 'Buyer Dossier & AI Sales', icon: <Building2 size={18} /> },
    { id: 'products', label: 'Digital Product Passports', icon: <Layers size={18} />, badge: 'DPP' },
    { id: 'documents', label: 'Export Document Vault', icon: <FileCheck size={18} />, badge: 'EUDR' },
    { id: 'shipments', label: 'Shipment Milestones & eBRC', icon: <Ship size={18} />, badge: 'Radar' },
    { id: 'customs', label: 'Ocean Displacements', icon: <Ship size={18} />, badge: 'Customs' },
    { id: 'analytics', label: 'Revenue & KPI Cockpit', icon: <BarChart3 size={18} /> },
    { id: 'verification', label: 'Analyst Verification Queue', icon: <CheckCircle size={18} />, badge: 'Audit' },
    { id: 'audit', label: 'Compliance Audit Trail', icon: <ShieldCheck size={18} />, badge: 'Insert-Only' },
  ];

  const sidebarContent = (
    <div className="flex flex-col justify-between h-full p-4 select-none">
      <div className="space-y-6">
        {/* App Branding */}
        <div className="flex items-center justify-between px-2 py-1">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-blue-600 via-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold shadow-md shadow-blue-500/20 text-lg">
              🌍
            </div>
            <div>
              <h1 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-1.5">
                Trade OS <span className="text-[10px] font-mono font-semibold px-1.5 py-0.2 bg-blue-100 text-blue-700 rounded-full">v2.0</span>
              </h1>
              <p className="text-[11px] text-slate-500 font-medium">India Export Revenue OS</p>
            </div>
          </div>

          {/* Close button on mobile drawer */}
          <button
            type="button"
            onClick={() => setMobileDrawerOpen(false)}
            className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100"
          >
            <X size={18} />
          </button>
        </div>

        {/* Primary Navigation */}
        <div className="space-y-1">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-3 mb-2">Export Workflows</p>
          {navItems.map((item) => {
            const active = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl font-medium text-sm transition-all cursor-pointer ${
                  active
                    ? 'bg-blue-50 text-blue-700 font-semibold border border-blue-200/80 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-200/50'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={active ? 'text-blue-600' : 'text-slate-400'}>{item.icon}</span>
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[10px] px-1.5 py-0.5 rounded-md font-mono font-semibold ${
                    active ? 'bg-blue-100 text-blue-700' : 'bg-slate-200/70 text-slate-600'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Exporter Readiness Profile Card in Sidebar */}
      <div
        onClick={() => setOnboardingModalOpen(true)}
        className="p-3.5 rounded-2xl bg-gradient-to-b from-white to-slate-50 border border-slate-200/80 shadow-xs space-y-2 cursor-pointer hover:border-blue-300 transition-all group"
      >
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-bold text-slate-900 tracking-tight group-hover:text-blue-600 transition-colors">
            Butler's Leather
          </span>
          <span className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700 font-bold border border-emerald-200/80 flex items-center gap-1">
            <CheckCircle size={10} /> 95/100
          </span>
        </div>
        <p className="text-[10px] text-slate-500 leading-relaxed font-medium">
          Ambur Cluster · DGFT & ICEGATE Verified · Click for profile
        </p>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Fixed Sidebar */}
      <aside className="hidden lg:flex w-64 glass-sidebar h-screen flex-col shrink-0 shadow-[1px_0_10px_rgba(0,0,0,0.02)]">
        {sidebarContent}
      </aside>

      {/* Mobile Drawer Backdrop & Drawer */}
      {isMobileDrawerOpen && (
        <div className="lg:hidden fixed inset-0 z-50 flex">
          <div
            className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs transition-opacity"
            onClick={() => setMobileDrawerOpen(false)}
          />
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-[#FBFBFC] shadow-2xl border-r border-slate-200 z-50">
            {sidebarContent}
          </div>
        </div>
      )}
    </>
  );
};
