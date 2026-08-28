import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/components/matches/ExporterProfileCard.tsx
w("frontend/src/components/matches/ExporterProfileCard.tsx", """import React from 'react';
import { Factory, ShieldCheck, MapPin } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { ExporterCapability } from '../../api/capability';

interface Props {
  capability?: ExporterCapability;
}

export const ExporterProfileCard: React.FC<Props> = ({ capability }) => {
  if (!capability) return null;

  return (
    <AppleCard variant="default" className="relative overflow-hidden border-blue-500/20 bg-gradient-to-r from-zinc-900/90 via-zinc-900/80 to-blue-950/20">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-3">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Factory size={22} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-white tracking-tight">{capability.company_name}</h2>
                <AppleBadge tone="blue" size="sm">Design Partner #1</AppleBadge>
                <AppleBadge tone="green" size="sm" dot>EUDR Ready</AppleBadge>
              </div>
              <p className="text-xs text-zinc-400 flex items-center gap-1.5 mt-0.5">
                <MapPin size={13} className="text-zinc-500" />
                <span>{capability.location}</span> · <span>{capability.cluster}</span>
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-2 text-xs">
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              🏭 Capacity: <b className="text-white font-mono">{capability.monthly_capacity_sqft.toLocaleString()} sqft/mo</b>
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              📦 MOQ: <b className="text-white font-mono">{capability.moq_sqft.toLocaleString()} sqft</b>
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              ⏱ Lead Time: <b className="text-white font-mono">{capability.lead_time_days} days</b> (Air Sample: {capability.sample_lead_time_days}d)
            </span>
            <span className="px-2.5 py-1 rounded-lg bg-zinc-800/80 text-zinc-300 border border-white/[0.05]">
              🚢 Port: <b className="text-white">{capability.port_of_export}</b>
            </span>
          </div>
        </div>

        <div className="flex items-center gap-4 p-4 rounded-xl bg-zinc-950/60 border border-white/[0.08] shrink-0">
          <div className="text-right">
            <p className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">EUDR Readiness</p>
            <p className="text-2xl font-bold font-mono text-emerald-400">{capability.eudr_readiness_score}<span className="text-sm text-zinc-500">/100</span></p>
            <p className="text-[10px] text-zinc-400">Due Diligence Ready</p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
            <ShieldCheck size={26} />
          </div>
        </div>
      </div>
    </AppleCard>
  );
};
""")

# 2. frontend/src/components/matches/MatchDriverBadge.tsx
w("frontend/src/components/matches/MatchDriverBadge.tsx", """import React from 'react';
import { CheckCircle2 } from 'lucide-react';
import { DriverItem } from '../../api/matches';

interface Props {
  driver: DriverItem;
}

export const MatchDriverBadge: React.FC<Props> = ({ driver }) => {
  return (
    <div className="group relative">
      <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-zinc-800/70 border border-white/[0.06] text-xs hover:border-blue-500/40 transition-colors cursor-help">
        <CheckCircle2 size={13} className="text-emerald-400 shrink-0" />
        <span className="text-zinc-300 font-medium">{driver.category}:</span>
        <span className="font-mono text-white font-semibold">{driver.score}/{driver.weight}</span>
      </div>

      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-2.5 bg-zinc-900 border border-white/[0.12] rounded-xl shadow-2xl text-[11px] text-zinc-300 opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity z-30">
        <p className="font-semibold text-white mb-0.5">{driver.title}</p>
        <p className="text-zinc-400">{driver.evidence}</p>
      </div>
    </div>
  );
};
""")

# 3. frontend/src/components/matches/MatchCard.tsx
w("frontend/src/components/matches/MatchCard.tsx", """import React from 'react';
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
""")

# 4. frontend/src/components/matches/MatchFilterBar.tsx
w("frontend/src/components/matches/MatchFilterBar.tsx", """import React from 'react';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';

interface Props {
  selectedGrade: string;
  onGradeChange: (grade: string) => void;
  selectedSegment: string;
  onSegmentChange: (seg: string) => void;
}

export const MatchFilterBar: React.FC<Props> = ({
  selectedGrade,
  onGradeChange,
  selectedSegment,
  onSegmentChange,
}) => {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 py-2">
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Match Grade:</span>
        <AppleSegmentedControl
          size="sm"
          value={selectedGrade}
          onChange={onGradeChange}
          options={[
            { value: 'ALL', label: 'All (5)' },
            { value: 'A', label: 'Grade A (2)' },
            { value: 'B', label: 'Grade B (3)' },
          ]}
        />
      </div>

      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Target Segment:</span>
        <AppleSegmentedControl
          size="sm"
          value={selectedSegment}
          onChange={onSegmentChange}
          options={[
            { value: 'ALL', label: 'All Segments' },
            { value: 'Bags', label: 'Leather Goods' },
            { value: 'Gloves', label: 'Luxury Gloves' },
            { value: 'Auto', label: 'Automotive' },
          ]}
        />
      </div>
    </div>
  );
};
""")

# 5. frontend/src/components/matches/MatchInspector.tsx
w("frontend/src/components/matches/MatchInspector.tsx", """import React from 'react';
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
""")

# 6. frontend/src/components/matches/MatchPortalView.tsx
w("frontend/src/components/matches/MatchPortalView.tsx", """import React, { useState } from 'react';
import { ExporterProfileCard } from './ExporterProfileCard';
import { MatchCard } from './MatchCard';
import { MatchFilterBar } from './MatchFilterBar';
import { MatchInspector } from './MatchInspector';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useMatches } from '../../hooks/useMatches';
import { useCapability } from '../../hooks/useCapability';

export const MatchPortalView: React.FC = () => {
  const { data: matchData, isLoading: isMatchesLoading } = useMatches();
  const { data: capability, isLoading: isCapLoading } = useCapability();

  const [selectedGrade, setSelectedGrade] = useState('ALL');
  const [selectedSegment, setSelectedSegment] = useState('ALL');

  if (isMatchesLoading || isCapLoading) {
    return <PageSkeleton />;
  }

  const matches = matchData?.matches || [];
  const filtered = matches.filter((m) => {
    if (selectedGrade !== 'ALL' && m.grade !== selectedGrade) return false;
    if (selectedSegment === 'Bags' && !m.segment.toLowerCase().includes('bag') && !m.segment.toLowerCase().includes('good')) return false;
    if (selectedSegment === 'Gloves' && !m.segment.toLowerCase().includes('glove')) return false;
    if (selectedSegment === 'Auto' && !m.segment.toLowerCase().includes('auto')) return false;
    return true;
  });

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <ExporterProfileCard capability={capability} />
      <MatchFilterBar
        selectedGrade={selectedGrade}
        onGradeChange={setSelectedGrade}
        selectedSegment={selectedSegment}
        onSegmentChange={setSelectedSegment}
      />
      <div className="space-y-4">
        {filtered.length === 0 ? (
          <EmptyState title="No buyers match current filter" description="Try selecting 'All' in the filter pills above." />
        ) : (
          filtered.map((m) => <MatchCard key={m.id} match={m} />)
        )}
      </div>
      <MatchInspector />
    </div>
  );
};
""")

print("[SUCCESS] Screen 1 (Match Portal) built successfully")
