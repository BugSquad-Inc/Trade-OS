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
            <h3 className="text-base font-bold text-slate-900 tracking-tight">EU & UK Market Requirement Readiness</h3>
            <AppleBadge tone="green" size="sm">Grade A Ready</AppleBadge>
          </div>
          <p className="text-xs text-slate-500 mt-0.5 font-medium">REACH SVHC, Chromium VI, LWG & Deforestation Traceability Gate</p>
        </div>
        <div className="text-right">
          <span className="text-2xl font-bold font-mono text-emerald-600">{scorecard.readiness_score}/100</span>
          <p className="text-[10px] text-slate-400 font-bold uppercase">Clearance Score</p>
        </div>
      </div>

      {/* Regulatory Context Banner */}
      <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 flex items-start gap-2.5">
        <CheckCircle size={16} className="text-emerald-600 shrink-0 mt-0.5" />
        <div>
          <p className="font-bold text-slate-900">Regulatory Framework (Updated 2026)</p>
          <p className="text-slate-600 text-[11px] mt-0.5 font-medium">
            Butler's Leather carries verified LWG Gold and REACH compliance. Farm-level geolocation dossiers remain active for high-tier German buyers.
          </p>
        </div>
      </div>

      <div className="p-3.5 rounded-xl bg-amber-50/90 border border-amber-200 text-xs text-amber-900 flex items-start gap-2.5">
        <AlertTriangle size={16} className="text-amber-600 shrink-0 mt-0.5" />
        <div>
          <p className="font-bold text-amber-900">Next Action to Reach 100/100: {scorecard.top_gap}</p>
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
