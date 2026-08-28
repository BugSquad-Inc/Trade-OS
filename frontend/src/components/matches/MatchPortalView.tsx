import React, { useState } from 'react';
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
