import React from 'react';
import { Sparkles, SlidersHorizontal } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const SimpleModeToggle: React.FC<{ className?: string }> = ({ className = '' }) => {
  const { isSimpleMode, toggleSimpleMode } = useUIStore();

  return (
    <button
      type="button"
      onClick={toggleSimpleMode}
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-xs font-semibold transition-all cursor-pointer select-none border ${
        isSimpleMode
          ? 'bg-blue-50/90 text-blue-700 border-blue-200/90 shadow-2xs hover:bg-blue-100/90'
          : 'bg-purple-50/90 text-purple-700 border-purple-200/90 shadow-2xs hover:bg-purple-100/90'
      } ${className}`}
      title={isSimpleMode ? 'Switch to Analyst Mode (raw scores, source IDs, weight breakdown)' : 'Switch to Simple Mode (executive summary for owners)'}
    >
      {isSimpleMode ? (
        <>
          <Sparkles className="w-3.5 h-3.5 text-blue-600" />
          <span>Simple Mode</span>
        </>
      ) : (
        <>
          <SlidersHorizontal className="w-3.5 h-3.5 text-purple-600" />
          <span>Analyst Mode</span>
        </>
      )}
    </button>
  );
};
