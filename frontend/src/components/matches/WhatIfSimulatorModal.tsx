import React, { useState } from 'react';
import { X, Sparkles, Sliders, CheckCircle2, AlertTriangle, ArrowRight, ShieldCheck, Ship, UserCheck } from 'lucide-react';
import { MatchCard } from '../../api/matches';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { AppleScoreRing } from '../apple/AppleScoreRing';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';

interface WhatIfSimulatorModalProps {
  match: MatchCard | null;
  isOpen: boolean;
  onClose: () => void;
}

export const WhatIfSimulatorModal: React.FC<WhatIfSimulatorModalProps> = ({
  match,
  isOpen,
  onClose,
}) => {
  if (!isOpen || !match) return null;

  // Simulator State adjustments
  const [hasCrViCert, setHasCrViCert] = useState<boolean>(!match.is_compliance_gate_failed);
  const [lwgRating, setLwgRating] = useState<'Gold' | 'Silver' | 'None'>('Gold');
  const [lightweightArticleAdded, setLightweightArticleAdded] = useState<boolean>(false);
  const [directContactVerified, setDirectContactVerified] = useState<boolean>(!!match.contact?.email);
  const [oceanBenchmarkLocked, setOceanBenchmarkLocked] = useState<boolean>(true);

  // Compute simulated scores
  let simProductFit = match.score_breakdown.product_fit + (lightweightArticleAdded ? 2.5 : 0.0);
  simProductFit = Math.min(25.0, simProductFit);

  let simCompliance = 0.0;
  let simGateFailed = false;
  if (!hasCrViCert) {
    simCompliance = 0.0;
    simGateFailed = true;
  } else {
    simCompliance = 20.0 + (lwgRating === 'Gold' ? 3.5 : lwgRating === 'Silver' ? 2.0 : 0.0);
  }
  simCompliance = Math.min(25.0, simCompliance);

  let simLane = 15.0 + (oceanBenchmarkLocked ? 3.0 : 0.0);
  simLane = Math.min(20.0, simLane);

  let simIntent = match.score_breakdown.intent_signals;
  
  let simAccessibility = 8.0 + (directContactVerified ? 5.5 : 0.0);
  simAccessibility = Math.min(15.0, simAccessibility);

  let simTotal = simGateFailed
    ? Math.min(38.0, simProductFit + simLane + simIntent + simAccessibility)
    : Math.round(simProductFit + simCompliance + simLane + simIntent + simAccessibility);

  const delta = Math.round(simTotal - match.total_score);

  const simGrade = simGateFailed ? 'D' : simTotal >= 85 ? 'A' : simTotal >= 70 ? 'B' : simTotal >= 55 ? 'C' : 'D';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="relative w-full max-w-2xl max-h-[85vh] bg-white rounded-3xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200/80 bg-slate-50/80 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center font-bold">
              <Sliders size={18} />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-2">
                What-If Match Simulator
                <AppleBadge tone="purple" size="sm">Explainability Engine v2.0</AppleBadge>
              </h2>
              <p className="text-xs text-slate-500 font-medium">
                Simulate how upgrading product specs, chemical certs, or freight terms changes your match score with <b>{match.name}</b>.
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">
          {/* Comparison Score Header */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded-2xl bg-gradient-to-r from-blue-50/60 to-purple-50/60 border border-blue-100">
            <div className="space-y-1">
              <span className="text-[10px] font-bold uppercase text-slate-500">Current Score</span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-bold font-mono text-slate-900">{match.total_score}</span>
                <span className="text-xs font-semibold text-slate-500">Grade {match.grade}</span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium">As evaluated from current factory certifications</p>
            </div>

            <div className="space-y-1 sm:text-right flex flex-col sm:items-end">
              <span className="text-[10px] font-bold uppercase text-purple-800">Simulated Score</span>
              <div className="flex items-baseline gap-2">
                <span className="text-2xl font-extrabold font-mono text-purple-900">{simTotal}</span>
                <span className={`text-xs font-bold font-mono ${delta >= 0 ? 'text-emerald-700' : 'text-rose-700'}`}>
                  {delta >= 0 ? `+${delta}` : delta} pts ({simGrade})
                </span>
              </div>
              <p className="text-[11px] text-purple-800 font-medium">Real-time projection across 5 dimensions</p>
            </div>
          </div>

          {/* Compliance Gate Warning if chemical cert unchecked */}
          {simGateFailed && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl flex items-start gap-2.5 text-xs text-rose-800">
              <AlertTriangle size={16} className="text-rose-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Non-Compensatory Gate Triggered:</span> Chemical safety failure (Cr VI &gt; 3.0 ppm or missing REACH) caps score to Grade D (&lt;38 pts).
              </div>
            </div>
          )}

          {/* Interactive Toggle Controls */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Adjust Factory Capabilities & Parameters
            </h4>

            <div className="space-y-2 text-xs">
              {/* 1. Chemical Safety Gate */}
              <label className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/80 hover:bg-slate-100/70 transition-colors cursor-pointer">
                <div className="flex items-center gap-2.5">
                  <ShieldCheck size={16} className={hasCrViCert ? 'text-emerald-600' : 'text-slate-400'} />
                  <div>
                    <span className="font-bold text-slate-900 block">Zero-Chromium VI & REACH Lab Certification</span>
                    <span className="text-slate-500 text-[11px]">Accredited TÜV test report confirming &lt;3.0 ppm Cr VI</span>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={hasCrViCert}
                  onChange={(e) => setHasCrViCert(e.target.checked)}
                  className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
              </label>

              {/* 2. LWG Environmental Audit */}
              <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <Sparkles size={16} className="text-amber-500" />
                  <div>
                    <span className="font-bold text-slate-900 block">Tannery LWG Environmental Rating</span>
                    <span className="text-slate-500 text-[11px]">Leather Working Group audited sustainability protocol</span>
                  </div>
                </div>
                <div className="flex items-center gap-1">
                  {(['None', 'Silver', 'Gold'] as const).map((lvl) => (
                    <button
                      key={lvl}
                      type="button"
                      onClick={() => setLwgRating(lvl)}
                      className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                        lwgRating === lvl
                          ? 'bg-amber-500 text-white shadow-2xs'
                          : 'bg-white text-slate-600 border border-slate-200'
                      }`}
                    >
                      {lvl}
                    </button>
                  ))}
                </div>
              </div>

              {/* 3. Product Matrix Article Overlap */}
              <label className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/80 hover:bg-slate-100/70 transition-colors cursor-pointer">
                <div className="flex items-center gap-2.5">
                  <CheckCircle2 size={16} className={lightweightArticleAdded ? 'text-blue-600' : 'text-slate-400'} />
                  <div>
                    <span className="font-bold text-slate-900 block">Add Lightweight Nappa (0.9-1.1mm) to Product Matrix</span>
                    <span className="text-slate-500 text-[11px]">Expands multi-article coverage for buyer luxury accessories</span>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={lightweightArticleAdded}
                  onChange={(e) => setLightweightArticleAdded(e.target.checked)}
                  className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
              </label>

              {/* 4. Direct Decision Maker Verified */}
              <label className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/80 hover:bg-slate-100/70 transition-colors cursor-pointer">
                <div className="flex items-center gap-2.5">
                  <UserCheck size={16} className={directContactVerified ? 'text-blue-600' : 'text-slate-400'} />
                  <div>
                    <span className="font-bold text-slate-900 block">Verified Direct Head of Sourcing Contact</span>
                    <span className="text-slate-500 text-[11px]">Direct validated email with GDPR legitimate interest justification</span>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={directContactVerified}
                  onChange={(e) => setDirectContactVerified(e.target.checked)}
                  className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
              </label>

              {/* 5. Freight Benchmark */}
              <label className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200/80 hover:bg-slate-100/70 transition-colors cursor-pointer">
                <div className="flex items-center gap-2.5">
                  <Ship size={16} className={oceanBenchmarkLocked ? 'text-teal-600' : 'text-slate-400'} />
                  <div>
                    <span className="font-bold text-slate-900 block">Lock Chennai-Hamburg Freight Rate ($1,850/FEU)</span>
                    <span className="text-slate-500 text-[11px]">Direct ocean carrier benchmark (28-day transit)</span>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={oceanBenchmarkLocked}
                  onChange={(e) => setOceanBenchmarkLocked(e.target.checked)}
                  className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
              </label>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex items-center justify-between shrink-0">
          <span>Mathematical explainability • No black-box weighting</span>
          <button
            type="button"
            onClick={onClose}
            className="px-3.5 py-1.5 bg-slate-200 hover:bg-slate-300 rounded-xl text-slate-700 font-bold transition-colors cursor-pointer"
          >
            Close Simulator
          </button>
        </div>
      </div>
    </div>
  );
};
