import React from 'react';
import { LayoutGrid, Radio, Building2, Ship, BarChart3 } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const GlassSidebar: React.FC = () => {
  const { currentView, setCurrentView } = useUIStore();

  const navItems = [
    { id: 'matches', label: 'Buyer Match Portal', icon: <LayoutGrid size={18} />, badge: '50+ Verified' },
    { id: 'signals', label: 'Live Market Signals', icon: <Radio size={18} />, badge: 'Live' },
    { id: 'accounts', label: 'Buyer Dossier & AI Sales', icon: <Building2 size={18} /> },
    { id: 'customs', label: 'Ocean Shipment Radar', icon: <Ship size={18} />, badge: 'Customs' },
    { id: 'analytics', label: 'Revenue & KPI Cockpit', icon: <BarChart3 size={18} /> },
  ];

  return (
    <aside className="w-64 glass-sidebar h-screen flex flex-col justify-between p-4 select-none shrink-0 shadow-[1px_0_10px_rgba(0,0,0,0.02)]">
      <div className="space-y-6">
        {/* App Branding */}
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-blue-600 via-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold shadow-md shadow-blue-500/20 text-lg">
            🌍
          </div>
          <div>
            <h1 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-1.5">
              Trade OS <span className="text-[10px] font-mono font-semibold px-1.5 py-0.2 bg-blue-100 text-blue-700 rounded-full">v1.0</span>
            </h1>
            <p className="text-[11px] text-slate-500 font-medium">Export Revenue OS</p>
          </div>
        </div>

        {/* Primary Navigation */}
        <div className="space-y-1">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-3 mb-2">Decision Views</p>
          {navItems.map((item) => {
            const active = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id as any)}
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

        {/* Wedge Corridor Info */}
        <div className="p-3.5 bg-white rounded-2xl border border-slate-200/80 shadow-xs space-y-2">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Active Export Wedge</p>
          <div className="text-xs space-y-1.5 text-slate-700">
            <div className="flex items-center justify-between font-semibold">
              <span>🇮🇳 Butler's Leather</span>
              <span className="text-slate-500 font-normal">Chennai</span>
            </div>
            <div className="flex items-center justify-between text-slate-500 text-[11px]">
              <span>→ 🇩🇪 German Buyers</span>
              <span className="font-medium text-slate-600">Hamburg</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Metrics */}
      <div className="p-3.5 bg-emerald-50 rounded-2xl border border-emerald-200/80 text-xs space-y-1 shadow-xs">
        <div className="flex items-center justify-between text-emerald-800 font-bold">
          <span>Sprint Target</span>
          <span>$500 Pilot</span>
        </div>
        <p className="text-[11px] text-emerald-700/90 font-medium">14-Day 5-Qualified-Match Guarantee</p>
      </div>
    </aside>
  );
};
