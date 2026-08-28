import React, { useState } from 'react';
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
