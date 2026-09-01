import React, { useState, useEffect } from 'react';
import { Search, Compass, Target, Package, DollarSign, Building2, FileText, ArrowRight, ShieldCheck, Ship, Sparkles, BookOpen, Layers, X } from 'lucide-react';
import { useUIStore, ViewType } from '../../store/uiStore';

interface CommandItem {
  id: string;
  title: string;
  category: string;
  icon: React.ReactNode;
  action: () => void;
  shortcut?: string;
}

export const CommandPaletteModal: React.FC = () => {
  const { isCommandPaletteOpen, setCommandPaletteOpen, setCurrentView, setGlossaryModalOpen } = useUIStore();
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);

  const commands: CommandItem[] = [
    {
      id: 'nav-today',
      title: 'Go to Today Cockpit (Actions & Radar)',
      category: 'Primary Views',
      icon: <Compass size={16} className="text-blue-500" />,
      shortcut: '1',
      action: () => setCurrentView('today'),
    },
    {
      id: 'nav-sales',
      title: 'Go to Sales Hub (Matches, Signals, Outreach)',
      category: 'Primary Views',
      icon: <Target size={16} className="text-indigo-500" />,
      shortcut: '2',
      action: () => setCurrentView('sales'),
    },
    {
      id: 'nav-orders',
      title: 'Go to Orders Hub (Deals & Shipment Tracking)',
      category: 'Primary Views',
      icon: <Package size={16} className="text-teal-500" />,
      shortcut: '3',
      action: () => setCurrentView('orders'),
    },
    {
      id: 'nav-money',
      title: 'Go to Money Hub (eBRC, Drawback, Invoices)',
      category: 'Primary Views',
      icon: <DollarSign size={16} className="text-emerald-500" />,
      shortcut: '4',
      action: () => setCurrentView('money'),
    },
    {
      id: 'nav-business',
      title: 'Go to My Business (Profile & DPP Matrix)',
      category: 'Primary Views',
      icon: <Building2 size={16} className="text-purple-500" />,
      shortcut: '5',
      action: () => setCurrentView('business'),
    },
    {
      id: 'nav-products',
      title: 'View Digital Product Passports & Specs',
      category: 'Expert Views',
      icon: <Layers size={16} className="text-blue-600" />,
      action: () => setCurrentView('products'),
    },
    {
      id: 'nav-verification',
      title: 'Open Analyst Verification Queue',
      category: 'Expert Views',
      icon: <ShieldCheck size={16} className="text-amber-500" />,
      action: () => setCurrentView('verification'),
    },
    {
      id: 'nav-documents',
      title: 'Generate Export Document Pack',
      category: 'Expert Views',
      icon: <FileText size={16} className="text-slate-600" />,
      action: () => setCurrentView('documents'),
    },
    {
      id: 'action-glossary',
      title: 'Open Plain-English Export Glossary',
      category: 'Help & Reference',
      icon: <BookOpen size={16} className="text-purple-600" />,
      shortcut: '?',
      action: () => setGlossaryModalOpen(true),
    },
  ];

  const filtered = commands.filter((c) =>
    c.title.toLowerCase().includes(query.toLowerCase()) ||
    c.category.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  const handleSelect = (cmd: CommandItem) => {
    cmd.action();
    setCommandPaletteOpen(false);
    setQuery('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % (filtered.length || 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + (filtered.length || 1)) % (filtered.length || 1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filtered[selectedIndex]) {
        handleSelect(filtered[selectedIndex]);
      }
    } else if (e.key === 'Escape') {
      e.preventDefault();
      setCommandPaletteOpen(false);
    }
  };

  if (!isCommandPaletteOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 p-4 bg-slate-900/50 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="relative w-full max-w-xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col">
        {/* Search Bar */}
        <div className="flex items-center gap-3 px-4 py-3.5 border-b border-slate-100 bg-slate-50/50">
          <Search size={18} className="text-slate-400 shrink-0" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a command or jump to view (e.g. Sales, Passports, Documents)..."
            className="w-full bg-transparent text-sm text-slate-900 placeholder:text-slate-400 outline-none font-medium"
          />
          <span className="px-1.5 py-0.5 rounded-md bg-slate-200 text-[10px] font-mono font-bold text-slate-600">ESC</span>
        </div>

        {/* Results List */}
        <div className="max-h-80 overflow-y-auto p-2 space-y-1">
          {filtered.length === 0 ? (
            <div className="py-8 text-center text-xs text-slate-400 font-medium">
              No matching commands found for "{query}".
            </div>
          ) : (
            filtered.map((cmd, idx) => {
              const isSelected = idx === selectedIndex;
              return (
                <div
                  key={cmd.id}
                  onClick={() => handleSelect(cmd)}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`flex items-center justify-between p-3 rounded-2xl cursor-pointer text-xs transition-all ${
                    isSelected
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'text-slate-700 hover:bg-slate-100'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`p-1.5 rounded-xl ${isSelected ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-700'}`}>
                      {cmd.icon}
                    </div>
                    <div>
                      <span className="font-bold block tracking-tight">{cmd.title}</span>
                      <span className={`text-[10px] ${isSelected ? 'text-blue-100' : 'text-slate-400'}`}>
                        {cmd.category}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {cmd.shortcut && (
                      <span className={`px-1.5 py-0.5 rounded-md text-[10px] font-mono font-bold ${
                        isSelected ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-500'
                      }`}>
                        {cmd.shortcut}
                      </span>
                    )}
                    <ArrowRight size={14} className={isSelected ? 'text-white' : 'text-slate-300'} />
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 border-t border-slate-100 bg-slate-50 text-[11px] text-slate-400 flex items-center justify-between font-mono">
          <span>Navigate with ↑ ↓ and Enter</span>
          <span>Trade OS Command Engine</span>
        </div>
      </div>
    </div>
  );
};
