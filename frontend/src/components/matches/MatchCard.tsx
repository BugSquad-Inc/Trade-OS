import React, { useState } from 'react';
import { Sparkles, MapPin, Mail, Sliders, AlertTriangle, ArrowUpRight } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleScoreRing } from '../apple/AppleScoreRing';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { MatchDriverBadge } from './MatchDriverBadge';
import { WhatIfSimulatorModal } from './WhatIfSimulatorModal';
import { MatchCard as MatchCardType } from '../../api/matches';
import { useUIStore } from '../../store/uiStore';

interface Props {
  match: MatchCardType;
}

export const MatchCard: React.FC<Props> = ({ match }) => {
  const { setSelectedBuyerId, setCurrentView, setSelectedInspectorMatch } = useUIStore();
  const [isSimulatorOpen, setIsSimulatorOpen] = useState(false);

  const handleOpenAccount = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedBuyerId(match.buyer_id);
    setCurrentView('accounts');
  };

  const handleOpenSimulator = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsSimulatorOpen(true);
  };

  const topCounterFactual = match.counter_factuals?.[0];

  return (
    <>
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
                <AppleBadge tone={match.grade === 'A' ? 'green' : match.grade === 'B' ? 'blue' : 'red'} size="sm">
                  Grade {match.grade} Match
                </AppleBadge>
                <TruthStatusBadge status="verified" sourceName="ICEGATE & Panjiva" />
                <span className="text-xs text-slate-500 font-medium flex items-center gap-1">
                  <MapPin size={12} className="text-slate-400" /> {match.city}, {match.country}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-1 font-medium">
                {match.segment} · <b className="text-slate-700">Annual Procurement Target: ~40k sqft</b>
              </p>
            </div>
          </div>

          <div className="shrink-0 text-right">
            <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Match Score (100pt)</div>
            <AppleScoreRing score={match.total_score} grade={match.grade} size={60} strokeWidth={5.5} />
          </div>
        </div>

        {/* Non-Compensatory Compliance Gate Warning (if triggered) */}
        {match.is_compliance_gate_failed && (
          <div className="p-2.5 bg-rose-50 border border-rose-200 rounded-xl flex items-center gap-2 text-xs text-rose-800 font-semibold">
            <AlertTriangle size={14} className="text-rose-600 shrink-0" />
            <span>Compliance Gate Failed: {match.compliance_gate_reason || 'Cr VI exceeds legal limit or missing REACH declaration.'}</span>
          </div>
        )}

        {/* 5-Dimension Score Drivers */}
        <div className="flex flex-wrap gap-2 pt-1">
          {match.drivers.map((d, i) => (
            <MatchDriverBadge key={i} driver={d} />
          ))}
        </div>

        {/* Counter-Factual Improvement Tip */}
        {topCounterFactual && (
          <div className="p-2.5 bg-purple-50/70 border border-purple-200/60 rounded-xl flex items-center justify-between gap-2 text-xs">
            <div className="flex items-center gap-2 text-purple-900">
              <Sparkles size={13} className="text-purple-600 shrink-0" />
              <span className="font-medium">
                <b>Score Opportunity:</b> {topCounterFactual.action} (<span className="text-emerald-700 font-bold">+{topCounterFactual.score_impact_pts} pts</span>)
              </span>
            </div>
            <button
              type="button"
              onClick={handleOpenSimulator}
              className="text-[11px] font-bold text-purple-700 hover:text-purple-900 hover:underline shrink-0 cursor-pointer"
            >
              Simulate &rarr;
            </button>
          </div>
        )}

        {/* Action Row */}
        <div className="p-3 bg-blue-50/80 rounded-xl border border-blue-200/70 flex items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-blue-900 truncate">
            <span className="font-semibold truncate">Next Action: {match.next_best_action}</span>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <AppleButton
              variant="secondary"
              size="sm"
              onClick={handleOpenSimulator}
              icon={<Sliders size={13} />}
            >
              What-If Simulator
            </AppleButton>
            <AppleButton
              variant="primary"
              size="sm"
              onClick={handleOpenAccount}
              icon={<Mail size={13} />}
            >
              Draft Pitch
            </AppleButton>
          </div>
        </div>
      </AppleCard>

      {/* Interactive Simulator Modal */}
      <WhatIfSimulatorModal
        match={match}
        isOpen={isSimulatorOpen}
        onClose={() => setIsSimulatorOpen(false)}
      />
    </>
  );
};
