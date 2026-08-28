import React from 'react';
import { CheckCircle, AlertTriangle } from 'lucide-react';
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
    <AppleCard variant="default" className="space-y-5 border-emerald-500/20 bg-white">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-base font-bold text-slate-900 tracking-tight">EUDR Regulation Readiness Audit</h3>
            <AppleBadge tone="orange" size="sm">Action Required</AppleBadge>
          </div>
          <p className="text-xs text-slate-500 mt-0.5 font-medium">EU Deforestation Regulation (EU 2023/1115) Compliance Matrix</p>
        </div>
        <div className="text-right">
          <span className="text-2xl font-bold font-mono text-emerald-600">{scorecard.readiness_score}/100</span>
          <p className="text-[10px] text-slate-400 font-bold uppercase">Readiness Score</p>
        </div>
      </div>

      <div className="p-3.5 rounded-xl bg-amber-50/90 border border-amber-200 text-xs text-amber-900 flex items-start gap-2.5">
        <AlertTriangle size={16} className="text-amber-600 shrink-0 mt-0.5" />
        <div>
          <p className="font-bold text-amber-900">Priority Gap: {scorecard.top_gap}</p>
          <p className="text-amber-700 text-[11px] mt-0.5 font-medium">Recommended: {scorecard.recommended_action}</p>
        </div>
      </div>

      <div className="space-y-2 text-xs">
        {scorecard.requirements.map((req, i) => (
          <div key={i} className="flex items-center justify-between p-2.5 rounded-lg bg-slate-50/90 border border-slate-200/80">
            <div className="flex items-center gap-2">
              {req.status === 'verified' ? (
                <CheckCircle size={15} className="text-emerald-600 shrink-0" />
              ) : (
                <AlertTriangle size={15} className="text-amber-600 shrink-0" />
              )}
              <span className="text-slate-800 font-medium">{req.item}</span>
            </div>
            <span className="font-mono text-slate-500 text-[11px] font-semibold">{req.article}</span>
          </div>
        ))}
      </div>
    </AppleCard>
  );
};
