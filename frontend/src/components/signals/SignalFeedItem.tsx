import React from 'react';
import { Quote } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { SignalItem } from '../../api/signals';

interface Props {
  signal: SignalItem;
}

export const SignalFeedItem: React.FC<Props> = ({ signal }) => {
  const toneMap: Record<string, 'red' | 'orange' | 'blue' | 'purple' | 'green'> = {
    critical: 'red',
    high: 'orange',
    medium: 'blue',
    low: 'green',
  };

  return (
    <AppleCard variant="default" className="space-y-3 bg-white hover:border-slate-300 transition-all">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <AppleBadge tone={toneMap[signal.severity] || 'blue'} size="sm">
            {signal.severity.toUpperCase()}
          </AppleBadge>
          <span className="text-xs font-bold text-slate-900 tracking-tight">{signal.company_name}</span>
          <span className="text-xs text-slate-400">·</span>
          <span className="text-xs text-slate-500 font-mono capitalize">{signal.category} Signal</span>
        </div>
        <span className="text-[11px] font-mono text-slate-400 font-medium">
          {new Date(signal.detected_at).toLocaleDateString()}
        </span>
      </div>

      <div>
        <h4 className="text-sm font-bold text-slate-900">{signal.title}</h4>
        <p className="text-xs text-slate-600 mt-1 leading-relaxed">{signal.summary}</p>
      </div>

      {signal.quote && (
        <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-xs text-slate-600 italic flex items-start gap-2">
          <Quote size={14} className="text-slate-400 shrink-0 mt-0.5" />
          <span>"{signal.quote}"</span>
        </div>
      )}
    </AppleCard>
  );
};
