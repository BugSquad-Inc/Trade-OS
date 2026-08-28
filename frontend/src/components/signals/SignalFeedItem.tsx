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
    <AppleCard variant="default" className="space-y-3">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <AppleBadge tone={toneMap[signal.severity] || 'blue'} size="sm">
            {signal.severity.toUpperCase()}
          </AppleBadge>
          <span className="text-xs font-bold text-white tracking-tight">{signal.company_name}</span>
          <span className="text-xs text-zinc-500">·</span>
          <span className="text-xs text-zinc-400 font-mono capitalize">{signal.category} Signal</span>
        </div>
        <span className="text-[11px] font-mono text-zinc-500">
          {new Date(signal.detected_at).toLocaleDateString()}
        </span>
      </div>

      <div>
        <h4 className="text-sm font-bold text-white">{signal.title}</h4>
        <p className="text-xs text-zinc-300 mt-1 leading-relaxed">{signal.summary}</p>
      </div>

      {signal.quote && (
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] text-xs text-zinc-400 italic flex items-start gap-2">
          <Quote size={14} className="text-zinc-600 shrink-0 mt-0.5" />
          <span>"{signal.quote}"</span>
        </div>
      )}
    </AppleCard>
  );
};
