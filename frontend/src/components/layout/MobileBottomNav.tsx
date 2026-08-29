import React from 'react';
import { LayoutGrid, Radio, Building2, Ship, BarChart3 } from 'lucide-react';
import { useUIStore, AppView } from '../../store/uiStore';

export const MobileBottomNav: React.FC = () => {
  const { currentView, setCurrentView } = useUIStore();

  const navItems: { id: AppView; label: string; icon: React.ReactNode }[] = [
    { id: 'matches', label: 'Buyers', icon: <LayoutGrid size={20} /> },
    { id: 'signals', label: 'Signals', icon: <Radio size={20} /> },
    { id: 'accounts', label: 'Dossiers', icon: <Building2 size={20} /> },
    { id: 'customs', label: 'Shipments', icon: <Ship size={20} /> },
    { id: 'analytics', label: 'Cockpit', icon: <BarChart3 size={20} /> },
  ];

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-xl border-t border-slate-200/90 shadow-[0_-4px_20px_rgba(0,0,0,0.05)] pb-[env(safe-area-inset-bottom)]">
      <div className="flex items-center justify-around h-16 px-2">
        {navItems.map((item) => {
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => setCurrentView(item.id)}
              className={`flex flex-col items-center justify-center flex-1 h-full min-w-[48px] min-h-[48px] py-1 transition-all rounded-xl cursor-pointer ${
                isActive
                  ? 'text-blue-600 font-bold'
                  : 'text-slate-500 hover:text-slate-800 font-medium'
              }`}
            >
              <div className={`relative p-1 rounded-xl transition-all ${isActive ? 'bg-blue-50 text-blue-600 scale-110' : ''}`}>
                {item.icon}
                {isActive && (
                  <span className="absolute -bottom-0.5 left-1/2 -translate-x-1/2 w-1 h-1 bg-blue-600 rounded-full" />
                )}
              </div>
              <span className="text-[10px] tracking-tight mt-0.5">{item.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
