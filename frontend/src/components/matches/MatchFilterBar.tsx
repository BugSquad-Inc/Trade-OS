import React from 'react';
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
