import React from 'react';
import { ShieldCheck, MapPin, CheckCircle, UserCheck, Mail } from 'lucide-react';
import { AppleDrawer } from '../apple/AppleDrawer';
import { AppleScoreRing } from '../apple/AppleScoreRing';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { MatchCard } from '../../api/matches';
import { useUIStore } from '../../store/uiStore';

export const MatchInspector: React.FC = () => {
  const { selectedInspectorMatch, isInspectorOpen, setInspectorOpen, setSelectedBuyerId, setCurrentView } = useUIStore();

  if (!selectedInspectorMatch) return null;
  const match: MatchCard = selectedInspectorMatch;

  const handleOpenAccount = () => {
    setInspectorOpen(false);
    setSelectedBuyerId(match.buyer_id);
    setCurrentView('accounts');
  };

  return (
    <AppleDrawer
      isOpen={isInspectorOpen}
      onClose={() => setInspectorOpen(false)}
      title={match.name}
      subtitle={`Rank #${match.rank} European Match Dossier · ${match.city}, ${match.country}`}
    >
      <div className="p-5 rounded-2xl bg-zinc-950/80 border border-white/[0.08] flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Total Match Score</span>
          <div className="text-3xl font-bold font-mono text-white mt-1">
            {match.total_score}<span className="text-base text-zinc-500">/100</span>
          </div>
          <p className="text-xs text-emerald-400 font-medium mt-1">Grade {match.grade} High Compatibility</p>
        </div>
        <AppleScoreRing score={match.total_score} grade={match.grade} size={76} strokeWidth={6.5} />
      </div>

      <div className="space-y-3">
        <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider">Score Breakdown & Evidence</h4>
        <div className="space-y-2">
          {match.drivers.map((d, i) => (
            <div key={i} className="p-3.5 rounded-xl bg-zinc-950/50 border border-white/[0.06] space-y-1">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-white flex items-center gap-1.5">
                  <CheckCircle size={14} className="text-emerald-400" />
                  {d.title} ({d.category})
                </span>
                <span className="font-mono text-blue-300 font-bold">{d.score} / {d.weight} pts</span>
              </div>
              <p className="text-xs text-zinc-400 pl-5 leading-relaxed">{d.evidence}</p>
            </div>
          ))}
        </div>
      </div>

      {match.contact && (
        <div className="p-4 rounded-xl bg-zinc-950/60 border border-white/[0.06] space-y-2">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
              <UserCheck size={14} className="text-blue-400" /> Verified Decision Maker
            </h4>
            <AppleBadge tone="green" size="sm">Confidence: {Math.round(match.contact.confidence * 100)}%</AppleBadge>
          </div>
          <div className="text-xs text-zinc-200">
            <p className="font-bold text-sm text-white">{match.contact.full_name}</p>
            <p className="text-zinc-400">{match.contact.title}</p>
            {match.contact.email && <p className="text-blue-400 font-mono mt-1">{match.contact.email}</p>}
          </div>
        </div>
      )}

      <div className="pt-4 border-t border-white/[0.08] flex items-center gap-3">
        <AppleButton
          variant="primary"
          className="w-full"
          icon={<Mail size={16} />}
          onClick={handleOpenAccount}
        >
          Compose AI Outreach Message
        </AppleButton>
      </div>
    </AppleDrawer>
  );
};
