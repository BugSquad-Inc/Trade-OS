import React from 'react';
import { ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { EUDRChecklistItem } from '../../api/signals';

interface Props {
  scorecard?: {
    entity: string;
    readiness_score: number;
    status: string;
    requirements: EUDRChecklistItem[];
    top_gap: string;
    recommended_action: string;
  };
}

export const EUDRScorecard: React.FC<Props> = ({ scorecard }) => {
  if (!scorecard) return null;

  return (
    <AppleCard variant="default" className="space-y-5 border-emerald-500/20">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-base font-bold text-white tracking-tight">EUDR Regulation Readiness Audit</h3>
            <AppleBadge tone="orange" size="sm">Action Required</AppleBadge>
          </div>
          <p className="text-xs text-zinc-400 mt-0.5">EU Deforestation Regulation (EU 2023/1115) Compliance Matrix</p>
        </div>
        <div className="text-right">
          <span className="text-2xl font-bold font-mono text-emerald-400">{scorecard.readiness_score}/100</span>
          <p className="text-[10px] text-zinc-400 font-semibold uppercase">Readiness Score</p>
        </div>
      </div>

      <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-200 flex items-start gap-2.5">
        <AlertTriangle size={16} className="text-amber-400 shrink-0 mt-0.5" />
        <div>
          <p className="font-semibold text-amber-100">Priority Gap: {scorecard.top_gap}</p>
          <p className="text-amber-300/80 text-[11px] mt-0.5">Recommended: {scorecard.recommended_action}</p>
        </div>
      </div>

      <div className="space-y-2 text-xs">
        {scorecard.requirements.map((req, i) => (
          <div key={i} className="flex items-center justify-between p-2.5 rounded-lg bg-zinc-950/60 border border-white/[0.05]">
            <div className="flex items-center gap-2">
              {req.status === 'verified' ? (
                <CheckCircle size={15} className="text-emerald-400 shrink-0" />
              ) : (
                <AlertTriangle size={15} className="text-amber-400 shrink-0" />
              )}
              <span className="text-zinc-200 font-medium">{req.item}</span>
            </div>
            <span className="font-mono text-zinc-400 text-[11px]">{req.article}</span>
          </div>
        ))}
      </div>
    </AppleCard>
  );
};
