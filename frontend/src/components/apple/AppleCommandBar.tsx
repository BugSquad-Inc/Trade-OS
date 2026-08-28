import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Building, ShieldCheck, ArrowRight } from 'lucide-react';
import { hybridSearchApi, SearchResultItem } from '../../api/search';

interface AppleCommandBarProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectBuyer: (id: string) => void;
  onNavigate: (view: 'matches' | 'signals' | 'accounts') => void;
}

export const AppleCommandBar: React.FC<AppleCommandBarProps> = ({
  isOpen,
  onClose,
  onSelectBuyer,
  onNavigate,
}) => {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResultItem[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else setQuery('');
      }
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  useEffect(() => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }
    const timer = setTimeout(async () => {
      setIsSearching(true);
      try {
        const res = await hybridSearchApi(query);
        setSearchResults(res.results);
      } catch (e) {
        console.error(e);
      } finally {
        setIsSearching(false);
      }
    }, 200);
    return () => clearTimeout(timer);
  }, [query]);

  const defaultNavigationItems = [
    { type: 'screen', id: 'matches', title: 'Match Portal', subtitle: 'View ranked European buyer matches', icon: <ArrowRight size={16} /> },
    { type: 'screen', id: 'signals', title: 'Signals & EUDR Feed', subtitle: 'Review EUDR 68/100 scorecard and freight benchmarks', icon: <ShieldCheck size={16} /> },
    { type: 'screen', id: 'accounts', title: 'Account 360 & AI Outreach', subtitle: 'Access deep buyer dossiers and agent workflows', icon: <Building size={16} /> },
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-slate-900/25 backdrop-blur-md"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -20 }}
            transition={{ type: 'spring', stiffness: 450, damping: 35 }}
            className="relative w-full max-w-2xl bg-white/95 border border-slate-200/90 rounded-2xl shadow-2xl backdrop-blur-3xl overflow-hidden z-10 text-slate-900"
          >
            <div className="flex items-center px-4 py-3.5 border-b border-slate-200/80 gap-3">
              <Search className="text-slate-400" size={20} />
              <input
                autoFocus
                type="text"
                placeholder="Search 50+ European buyers, HS codes, or natural queries (e.g. 'handbag leather')..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full bg-transparent text-slate-900 placeholder-slate-400 focus:outline-none text-base font-normal"
              />
              <span className="text-[11px] font-mono px-2 py-0.5 bg-slate-100 text-slate-500 rounded-md border border-slate-200">
                ESC
              </span>
            </div>

            <div className="max-h-96 overflow-y-auto p-2 space-y-1">
              {query.trim() && searchResults.length > 0 ? (
                searchResults.map((item) => (
                  <div
                    key={item.company_id}
                    onClick={() => {
                      onSelectBuyer(item.company_id);
                      onClose();
                    }}
                    className="flex items-center justify-between p-3 rounded-xl hover:bg-slate-100/90 cursor-pointer transition-colors group"
                  >
                    <div className="flex items-center gap-3">
                      <span className="p-2 rounded-lg bg-slate-100 text-blue-600 group-hover:bg-blue-100 group-hover:text-blue-700 transition-colors">
                        <Building size={16} />
                      </span>
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="text-sm font-bold text-slate-900 group-hover:text-blue-600">{item.canonical_name}</h4>
                          <span className="text-[10px] font-mono font-semibold px-1.5 py-0.2 bg-blue-50 text-blue-700 rounded">
                            RRF: {item.rrf_score}
                          </span>
                        </div>
                        <p className="text-xs text-slate-500">{item.segment} · {item.city || item.country_code}</p>
                        <p className="text-[11px] text-slate-400 italic mt-0.5">{item.relevance_explanation}</p>
                      </div>
                    </div>
                    <span className="text-xs text-slate-400 group-hover:text-blue-600 font-medium">Inspect →</span>
                  </div>
                ))
              ) : (
                defaultNavigationItems.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => {
                      onNavigate(item.id as any);
                      onClose();
                    }}
                    className="flex items-center justify-between p-3 rounded-xl hover:bg-slate-100/90 cursor-pointer transition-colors group"
                  >
                    <div className="flex items-center gap-3">
                      <span className="p-2 rounded-lg bg-slate-100 text-slate-600 group-hover:bg-blue-100 group-hover:text-blue-700 transition-colors">
                        {item.icon}
                      </span>
                      <div>
                        <h4 className="text-sm font-bold text-slate-900 group-hover:text-blue-600">{item.title}</h4>
                        <p className="text-xs text-slate-500">{item.subtitle}</p>
                      </div>
                    </div>
                    <span className="text-xs text-slate-400 group-hover:text-blue-600 font-medium">Select →</span>
                  </div>
                ))
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
