import React from 'react';
import { RefreshCw } from 'lucide-react';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';
import { AppleButton } from '../apple/AppleButton';
import { usePipelineRefresh } from '../../hooks/useIngest';

interface Props {
  selectedGrade: string;
  onGradeChange: (grade: string) => void;
  selectedCountry: string;
  onCountryChange: (country: string) => void;
  totalCount: number;
}

export const MatchFilterBar: React.FC<Props> = ({
  selectedGrade,
  onGradeChange,
  selectedCountry,
  onCountryChange,
  totalCount,
}) => {
  const { mutate: refreshPipeline, isPending } = usePipelineRefresh();

  return (
    <div className="flex flex-wrap items-center justify-between gap-4 py-2">
      <div className="flex flex-wrap items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Country:</span>
          <AppleSegmentedControl
            size="sm"
            value={selectedCountry}
            onChange={onCountryChange}
            options={[
              { value: 'ALL', label: `All Europe (${totalCount})` },
              { value: 'DE', label: 'Germany 🇩🇪' },
              { value: 'IT', label: 'Italy 🇮🇹' },
              { value: 'FR', label: 'France 🇫🇷' },
              { value: 'ES', label: 'Spain 🇪🇸' },
              { value: 'UK', label: 'UK 🇬🇧' },
            ]}
          />
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-zinc-400 uppercase tracking-wider">Grade:</span>
          <AppleSegmentedControl
            size="sm"
            value={selectedGrade}
            onChange={onGradeChange}
            options={[
              { value: 'ALL', label: 'All Grades' },
              { value: 'A', label: 'Grade A' },
              { value: 'B', label: 'Grade B' },
            ]}
          />
        </div>
      </div>

      <AppleButton
        variant="glass"
        size="sm"
        loading={isPending}
        onClick={() => refreshPipeline()}
        icon={<RefreshCw size={13} className={isPending ? 'animate-spin' : ''} />}
      >
        Refresh Pipeline
      </AppleButton>
    </div>
  );
};
