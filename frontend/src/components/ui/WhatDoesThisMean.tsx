import React from 'react';
import { HelpCircle } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

interface WhatDoesThisMeanProps {
  term: string;
  className?: string;
  label?: string;
}

export const WhatDoesThisMean: React.FC<WhatDoesThisMeanProps> = ({
  term,
  className = '',
  label = 'What does this mean?'
}) => {
  const { openGlossary } = useUIStore();

  return (
    <button
      type="button"
      onClick={(e) => {
        e.stopPropagation();
        openGlossary(term);
      }}
      className={`inline-flex items-center gap-1 text-[11px] font-medium text-blue-600 hover:text-blue-700 hover:underline cursor-pointer transition-colors ${className}`}
      title={`Click to read plain-English explanation for "${term}"`}
    >
      <HelpCircle className="w-3.5 h-3.5" />
      <span>{label}</span>
    </button>
  );
};
