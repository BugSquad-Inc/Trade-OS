import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/components/signals/EUDRScorecard.tsx
w("frontend/src/components/signals/EUDRScorecard.tsx", """import React from 'react';
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
""")

# 2. frontend/src/components/signals/REACHComplianceCard.tsx
w("frontend/src/components/signals/REACHComplianceCard.tsx", """import React from 'react';
import { FlaskConical, CheckCircle2 } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';

export const REACHComplianceCard: React.FC = () => {
  const tests = [
    { substance: 'Chromium VI (Cr VI)', threshold: '< 3.0 ppm', result: 'Non-Detectable (PASS)' },
    { substance: 'Banned Azo Dyes', threshold: '< 30 ppm', result: 'Non-Detectable (PASS)' },
    { substance: 'Pentachlorophenol (PCP)', threshold: '< 0.5 ppm', result: 'PASS (0.05 ppm)' },
    { substance: 'Formaldehyde Content', threshold: '< 20 ppm', result: 'PASS (8.2 ppm)' },
  ];

  return (
    <AppleCard variant="default" className="space-y-4 border-blue-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <FlaskConical size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">EU REACH SVHC Chemical Safety</h3>
            <p className="text-xs text-zinc-400">TUV Rheinland & Eurofins Laboratory Verified</p>
          </div>
        </div>
        <AppleBadge tone="green" size="sm" dot>100% Certified</AppleBadge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
        {tests.map((t, i) => (
          <div key={i} className="p-2.5 rounded-lg bg-zinc-950/60 border border-white/[0.05] flex items-center justify-between">
            <div>
              <p className="font-semibold text-zinc-200">{t.substance}</p>
              <p className="text-[10px] text-zinc-500">Limit: {t.threshold}</p>
            </div>
            <span className="text-[11px] font-mono text-emerald-400 font-semibold">{t.result}</span>
          </div>
        ))}
      </div>
    </AppleCard>
  );
};
""")

# 3. frontend/src/components/signals/FreightLaneWidget.tsx
w("frontend/src/components/signals/FreightLaneWidget.tsx", """import React from 'react';
import { Ship } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';

interface Props {
  benchmark?: {
    origin_port: string;
    destination_port: string;
    mode: string;
    container_type: string;
    rate_usd: number;
    rate_spread: string;
    transit_days: string;
    port_congestion_index: string;
    reroute_risk_notes?: string;
    sample_air_transit: string;
  };
}

export const FreightLaneWidget: React.FC<Props> = ({ benchmark }) => {
  if (!benchmark) return null;

  return (
    <AppleCard variant="default" className="space-y-4 border-teal-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-teal-500/10 text-teal-400 border border-teal-500/20">
            <Ship size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">Chennai → Hamburg Trade Corridor</h3>
            <p className="text-xs text-zinc-400">Ocean Freight & Landed Cost Economics</p>
          </div>
        </div>
        <AppleBadge tone="teal" size="sm">Active Benchmark</AppleBadge>
      </div>

      <div className="grid grid-cols-3 gap-3 text-center">
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05]">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase">Spot Rate (40HC)</p>
          <p className="text-lg font-bold font-mono text-teal-300 mt-0.5">${benchmark.rate_usd.toLocaleString()}</p>
          <p className="text-[10px] text-zinc-500">{benchmark.rate_spread}</p>
        </div>
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05]">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase">Ocean Transit</p>
          <p className="text-lg font-bold font-mono text-white mt-0.5">{benchmark.transit_days}</p>
          <p className="text-[10px] text-zinc-500">Port to Port</p>
        </div>
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05]">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase">Air Sample</p>
          <p className="text-lg font-bold font-mono text-blue-300 mt-0.5">{benchmark.sample_air_transit}</p>
          <p className="text-[10px] text-zinc-500">To Frankfurt (FRA)</p>
        </div>
      </div>
    </AppleCard>
  );
};
""")

# 4. frontend/src/components/signals/SignalFeedItem.tsx
w("frontend/src/components/signals/SignalFeedItem.tsx", """import React from 'react';
import { Quote } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { SignalItem } from '../../api/signals';

interface Props {
  signal: SignalItem;
}

export const SignalFeedItem: React.FC<Props> = ({ signal }) => {
  const toneMap: Record<string, 'red' | 'orange' | 'blue' | 'purple' | 'green'> = {
    critical: 'red',
    high: 'orange',
    medium: 'blue',
    low: 'green',
  };

  return (
    <AppleCard variant="default" className="space-y-3">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2.5">
          <AppleBadge tone={toneMap[signal.severity] || 'blue'} size="sm">
            {signal.severity.toUpperCase()}
          </AppleBadge>
          <span className="text-xs font-bold text-white tracking-tight">{signal.company_name}</span>
          <span className="text-xs text-zinc-500">·</span>
          <span className="text-xs text-zinc-400 font-mono capitalize">{signal.category} Signal</span>
        </div>
        <span className="text-[11px] font-mono text-zinc-500">
          {new Date(signal.detected_at).toLocaleDateString()}
        </span>
      </div>

      <div>
        <h4 className="text-sm font-bold text-white">{signal.title}</h4>
        <p className="text-xs text-zinc-300 mt-1 leading-relaxed">{signal.summary}</p>
      </div>

      {signal.quote && (
        <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] text-xs text-zinc-400 italic flex items-start gap-2">
          <Quote size={14} className="text-zinc-600 shrink-0 mt-0.5" />
          <span>"{signal.quote}"</span>
        </div>
      )}
    </AppleCard>
  );
};
""")

# 5. frontend/src/components/signals/SignalsView.tsx
w("frontend/src/components/signals/SignalsView.tsx", """import React, { useState } from 'react';
import { EUDRScorecard } from './EUDRScorecard';
import { REACHComplianceCard } from './REACHComplianceCard';
import { FreightLaneWidget } from './FreightLaneWidget';
import { SignalFeedItem } from './SignalFeedItem';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';
import { PageSkeleton } from '../ui/PageSkeleton';
import { useSignals } from '../../hooks/useSignals';

export const SignalsView: React.FC = () => {
  const { data, isLoading } = useSignals();
  const [selectedCategory, setSelectedCategory] = useState('ALL');

  if (isLoading) return <PageSkeleton />;

  const signals = data?.signals || [];
  const filtered = selectedCategory === 'ALL'
    ? signals
    : signals.filter(s => s.category.toLowerCase() === selectedCategory.toLowerCase());

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <EUDRScorecard scorecard={data?.eudr_scorecard} />
        <div className="space-y-6">
          <FreightLaneWidget benchmark={data?.freight_benchmark} />
          <REACHComplianceCard />
        </div>
      </div>

      <div className="space-y-4 pt-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-white tracking-tight">Live Intelligence Stream</h3>
          <AppleSegmentedControl
            size="sm"
            value={selectedCategory}
            onChange={setSelectedCategory}
            options={[
              { value: 'ALL', label: 'All Signals' },
              { value: 'compliance', label: 'Compliance' },
              { value: 'intent', label: 'Buyer Intent' },
              { value: 'regulatory', label: 'Regulatory' },
            ]}
          />
        </div>

        <div className="space-y-3">
          {filtered.map(s => (
            <SignalFeedItem key={s.id} signal={s} />
          ))}
        </div>
      </div>
    </div>
  );
};
""")

print("[SUCCESS] Screen 2 (Signals & Compliance) built successfully")
