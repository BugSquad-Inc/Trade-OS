import React from 'react';
import { Sparkles, MapPin, Mail } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleScoreRing } from '../apple/AppleScoreRing';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { MatchDriverBadge } from './MatchDriverBadge';
import { MatchCard as MatchCardType } from '../../api/matches';
import { useUIStore } from '../../store/uiStore';

interface Props {
  match: MatchCardType;
}

export const MatchCard: React.FC<Props> = ({ match }) => {
  const { setSelectedBuyerId, setCurrentView, setSelectedInspectorMatch } = useUIStore();

  const handleOpenAccount = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedBuyerId(match.buyer_id);
    setCurrentView('accounts');
  };

  return (
    <AppleCard
      variant="default"
      hoverable
      onClick={() => setSelectedInspectorMatch(match)}
      className="space-y-4 cursor-pointer hover:border-white/[0.15] transition-all"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-2xl bg-zinc-800/80 border border-white/[0.08] text-white font-bold flex items-center justify-center text-lg shrink-0">
            #{match.rank}
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-lg font-bold text-white tracking-tight">{match.name}</h3>
              <AppleBadge tone={match.grade === 'A' ? 'green' : 'blue'} size="sm">
                Grade {match.grade} Match
              </AppleBadge>
              <span className="text-xs text-zinc-400 flex items-center gap-1">
                <MapPin size={12} /> {match.city}, {match.country}
              </span>
            </div>
            <p className="text-xs text-zinc-400 mt-1 font-medium">{match.segment}</p>
          </div>
        </div>

        <div className="shrink-0">
          <AppleScoreRing score={match.total_score} grade={match.grade} size={64} strokeWidth={5.5} />
        </div>
      </div>

      <div className="flex flex-wrap gap-2 pt-1">
        {match.drivers.map((d, i) => (
          <MatchDriverBadge key={i} driver={d} />
        ))}
      </div>

      <div className="p-3 bg-blue-500/10 rounded-xl border border-blue-500/20 flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 text-blue-200">
          <Sparkles size={14} className="text-blue-400 shrink-0" />
          <span className="font-medium">Next Action: {match.next_best_action}</span>
        </div>
        <AppleButton
          variant="primary"
          size="sm"
          onClick={handleOpenAccount}
          icon={<Mail size={13} />}
        >
          Outreach
        </AppleButton>
      </div>
    </AppleCard>
  );
};
