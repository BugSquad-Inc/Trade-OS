import React, { useState } from 'react';
import { CheckCircle, UserCheck, Mail, Sparkles, Sliders, AlertTriangle } from 'lucide-react';
import { AppleDrawer } from '../apple/AppleDrawer';
import { AppleScoreRing } from '../apple/AppleScoreRing';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { WhatIfSimulatorModal } from './WhatIfSimulatorModal';
import { MatchCard } from '../../api/matches';
import { useUIStore } from '../../store/uiStore';

export const MatchInspector: React.FC = () => {
  const { selectedInspectorMatch, isInspectorOpen, setInspectorOpen, setSelectedBuyerId, setCurrentView } = useUIStore();
  const [isSimulatorOpen, setIsSimulatorOpen] = useState(false);

  if (!selectedInspectorMatch) return null;
  const match: MatchCard = selectedInspectorMatch;

  const handleOpenAccount = () => {
    setInspectorOpen(false);
    setSelectedBuyerId(match.buyer_id);
    setCurrentView('accounts');
  };

  return (
    <>
      <AppleDrawer
        isOpen={isInspectorOpen}
        onClose={() => setInspectorOpen(false)}
        title={match.name}
        subtitle={`Rank #${match.rank} European Match Dossier · ${match.city}, ${match.country}`}
      >
        <div className="space-y-5">
          {/* Match Score Summary */}
          <div className="p-5 rounded-2xl bg-white border border-slate-200/90 shadow-sm flex items-center justify-between">
            <div>
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">100-Point Match Score</span>
              <div className="text-3xl font-bold font-mono text-slate-900 mt-1">
                {match.total_score}<span className="text-base text-slate-400">/100</span>
              </div>
              <p className="text-xs text-emerald-600 font-semibold mt-1">Grade {match.grade} High Compatibility</p>
              <p className="text-[10px] font-mono text-slate-400 mt-0.5">Engine: {match.score_version || 'v2.0-product-matrix'}</p>
            </div>
            <AppleScoreRing score={match.total_score} grade={match.grade} size={76} strokeWidth={6.5} />
          </div>

          {/* Compliance Gate Warning if triggered */}
          {match.is_compliance_gate_failed && (
            <div className="p-3.5 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 space-y-1">
              <div className="flex items-center gap-2 font-bold">
                <AlertTriangle size={15} className="text-rose-600 shrink-0" />
                <span>Non-Compensatory Compliance Gate Failed</span>
              </div>
              <p className="text-[11px] text-rose-700">
                {match.compliance_gate_reason || 'Chemical safety check failed. Score is capped to Grade D until zero-Cr VI certificate is attached.'}
              </p>
            </div>
          )}

          {/* Counter-Factual Improvement Suggestions */}
          {match.counter_factuals && match.counter_factuals.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles size={14} className="text-purple-600" /> Counter-Factual Recommendations
              </h4>
              <div className="space-y-2">
                {match.counter_factuals.map((cf, i) => (
                  <div key={i} className="p-3 bg-purple-50/60 rounded-xl border border-purple-200/70 text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-purple-950">{cf.action}</span>
                      <span className="font-mono font-bold text-emerald-700">+{cf.score_impact_pts} pts</span>
                    </div>
                    <p className="text-[11px] text-slate-600">{cf.implementation_tip}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 5-Dimension Score Breakdown */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Score Breakdown & Evidence</h4>
            <div className="space-y-2">
              {match.drivers.map((d, i) => (
                <div key={i} className="p-3.5 rounded-xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
                  <div className="flex items-center justify-between text-xs font-semibold">
                    <span className="text-slate-900 flex items-center gap-1.5 font-bold">
                      <CheckCircle size={14} className="text-emerald-600" />
                      {d.title} ({d.category})
                    </span>
                    <span className="font-mono text-blue-700 font-bold">{d.score} / {d.weight} pts</span>
                  </div>
                  <p className="text-xs text-slate-600 pl-5 leading-relaxed">{d.evidence}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Verified Contact Card */}
          {match.contact && (
            <div className="p-4 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-2">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                  <UserCheck size={14} className="text-blue-600" /> Verified Decision Maker
                </h4>
                <AppleBadge tone="green" size="sm">Confidence: {Math.round(match.contact.confidence * 100)}%</AppleBadge>
              </div>
              <div className="text-xs text-slate-700">
                <p className="font-bold text-sm text-slate-900">{match.contact.full_name}</p>
                <p className="text-slate-500">{match.contact.title}</p>
                {match.contact.email && <p className="text-blue-600 font-mono font-medium mt-1">{match.contact.email}</p>}
              </div>
            </div>
          )}

          {/* Action Row */}
          <div className="pt-4 border-t border-slate-200/80 flex items-center gap-3">
            <AppleButton
              variant="secondary"
              className="flex-1"
              icon={<Sliders size={15} />}
              onClick={() => setIsSimulatorOpen(true)}
            >
              What-If Simulator
            </AppleButton>
            <AppleButton
              variant="primary"
              className="flex-1"
              icon={<Mail size={15} />}
              onClick={handleOpenAccount}
            >
              Draft Outreach
            </AppleButton>
          </div>
        </div>
      </AppleDrawer>

      {/* Simulator Modal */}
      <WhatIfSimulatorModal
        match={match}
        isOpen={isSimulatorOpen}
        onClose={() => setIsSimulatorOpen(false)}
      />
    </>
  );
};
