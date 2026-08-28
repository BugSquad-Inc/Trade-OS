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
      className="space-y-4 cursor-pointer hover:border-blue-400/50 hover:shadow-md transition-all bg-white"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-2xl bg-slate-100 text-slate-800 border border-slate-200 font-bold flex items-center justify-center text-lg shrink-0 shadow-2xs font-mono">
            #{match.rank}
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-lg font-bold text-slate-900 tracking-tight">{match.name}</h3>
              <AppleBadge tone={match.grade === 'A' ? 'green' : 'blue'} size="sm">
                Grade {match.grade} Match
              </AppleBadge>
              <AppleBadge tone="teal" size="sm">
                AW26 Sourcing
              </AppleBadge>
              <span className="text-xs text-slate-500 font-medium flex items-center gap-1">
                <MapPin size={12} className="text-slate-400" /> {match.city}, {match.country}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-medium">
              {match.segment} · <b className="text-emerald-700">Est. Annual Order: ~40k sqft (€160,000)</b>
            </p>
          </div>
        </div>

        <div className="shrink-0 text-right">
          <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Match Confidence</div>
          <AppleScoreRing score={match.total_score} grade={match.grade} size={60} strokeWidth={5.5} />
        </div>
      </div>

      <div className="flex flex-wrap gap-2 pt-1">
        {match.drivers.map((d, i) => (
          <MatchDriverBadge key={i} driver={d} />
        ))}
      </div>

      <div className="p-3 bg-blue-50/80 rounded-xl border border-blue-200/70 flex items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 text-blue-900">
          <Sparkles size={14} className="text-blue-600 shrink-0" />
          <span className="font-semibold">Recommended Action: {match.next_best_action}</span>
        </div>
        <AppleButton
          variant="primary"
          size="sm"
          onClick={handleOpenAccount}
          icon={<Mail size={13} />}
        >
          Draft Sample Pitch
        </AppleButton>
      </div>
    </AppleCard>
  );
};
