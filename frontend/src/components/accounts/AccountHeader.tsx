import React from 'react';
import { MapPin } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleScoreRing } from '../apple/AppleScoreRing';
import { Account360 } from '../../api/accounts';

interface Props {
  account: Account360;
}

export const AccountHeader: React.FC<Props> = ({ account }) => {
  return (
    <AppleCard variant="default" className="space-y-4 border-blue-500/20">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-zinc-800 text-white font-bold text-xl border border-white/[0.08]">
              {account.rank ? `#${account.rank}` : '🇩🇪'}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-2xl font-bold text-white tracking-tight">{account.canonical_name}</h2>
                {account.grade && <AppleBadge tone="green" size="sm">Grade {account.grade} Fit</AppleBadge>}
              </div>
              <p className="text-xs text-zinc-400 flex items-center gap-2 mt-0.5">
                <MapPin size={13} className="text-zinc-500" />
                <span>{account.city}, {account.country}</span> · <span className="text-zinc-300 font-medium">{account.segment}</span>
              </p>
            </div>
          </div>

          <p className="text-xs text-zinc-300 max-w-2xl leading-relaxed">{account.description}</p>
        </div>

        {account.match_score && (
          <div className="shrink-0 flex items-center gap-4 p-4 rounded-xl bg-zinc-950/60 border border-white/[0.08]">
            <div className="text-right">
              <span className="text-xs font-semibold text-zinc-400 uppercase">Match Score</span>
              <p className="text-2xl font-bold font-mono text-white">{account.match_score}<span className="text-xs text-zinc-500">/100</span></p>
            </div>
            <AppleScoreRing score={account.match_score} grade={account.grade} size={58} strokeWidth={5} />
          </div>
        )}
      </div>
    </AppleCard>
  );
};
