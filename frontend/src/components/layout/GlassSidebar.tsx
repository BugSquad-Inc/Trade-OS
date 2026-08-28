import React from 'react';
import { LayoutGrid, Radio, Building2, ShieldCheck, Ship, ArrowUpRight } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const GlassSidebar: React.FC = () => {
  const { currentView, setCurrentView } = useUIStore();

  const navItems = [
    { id: 'matches', label: 'Match Portal', icon: <LayoutGrid size={18} />, badge: '5 Qualified' },
    { id: 'signals', label: 'Live Signals & EUDR', icon: <Radio size={18} />, badge: 'Live' },
    { id: 'accounts', label: 'Account 360', icon: <Building2 size={18} /> },
  ];

  return (
    <aside className="w-64 glass-sidebar h-screen flex flex-col justify-between p-4 select-none shrink-0">
      <div className="space-y-6">
        {/* App Branding */}
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/25">
            🌍
          </div>
          <div>
            <h1 className="text-sm font-bold text-white tracking-tight flex items-center gap-1.5">
              Trade OS <span className="text-[10px] font-mono px-1.5 py-0.2 bg-blue-500/20 text-blue-300 rounded-full">v1.0</span>
            </h1>
            <p className="text-[11px] text-zinc-400">Export Revenue OS</p>
          </div>
        </div>

        {/* Primary Navigation */}
        <div className="space-y-1">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider px-3 mb-2">Decision Views</p>
          {navItems.map((item) => {
            const active = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id as any)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl font-medium text-sm transition-all cursor-pointer ${
                  active
                    ? 'bg-blue-600/15 text-blue-300 border border-blue-500/30 shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={active ? 'text-blue-400' : 'text-zinc-400'}>{item.icon}</span>
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[10px] px-1.5 py-0.5 rounded-md font-mono ${
                    active ? 'bg-blue-500/30 text-blue-200' : 'bg-zinc-800 text-zinc-400'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Wedge Corridor Info */}
        <div className="p-3 bg-zinc-900/60 rounded-xl border border-white/[0.06] space-y-2">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider">Active Export Wedge</p>
          <div className="text-xs space-y-1 text-zinc-300">
            <div className="flex items-center justify-between font-medium">
              <span>🇮🇳 Butler's Leather</span>
              <span className="text-zinc-400">Chennai</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400 text-[11px]">
              <span>→ 🇩🇪 German Buyers</span>
              <span>Hamburg</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Metrics */}
      <div className="p-3 bg-emerald-500/10 rounded-xl border border-emerald-500/20 text-xs space-y-1">
        <div className="flex items-center justify-between text-emerald-300 font-semibold">
          <span>Sprint Target</span>
          <span>$500 Pilot</span>
        </div>
        <p className="text-[11px] text-zinc-400">14-Day 5-Qualified-Match Guarantee</p>
      </div>
    </aside>
  );
};
