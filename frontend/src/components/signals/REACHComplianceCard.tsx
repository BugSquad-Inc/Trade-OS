import React from 'react';
import { FlaskConical } from 'lucide-react';
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
    <AppleCard variant="default" className="space-y-4 border-blue-500/20 bg-white">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-blue-50 text-blue-600 border border-blue-200/80 shadow-2xs">
            <FlaskConical size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 tracking-tight">EU REACH SVHC Chemical Safety</h3>
            <p className="text-xs text-slate-500 font-medium">TUV Rheinland & Eurofins Laboratory Verified</p>
          </div>
        </div>
        <AppleBadge tone="green" size="sm" dot>100% Certified</AppleBadge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
        {tests.map((t, i) => (
          <div key={i} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between shadow-2xs">
            <div>
              <p className="font-bold text-slate-800">{t.substance}</p>
              <p className="text-[10px] text-slate-500 font-medium">Limit: {t.threshold}</p>
            </div>
            <span className="text-[11px] font-mono text-emerald-700 font-bold">{t.result}</span>
          </div>
        ))}
      </div>
    </AppleCard>
  );
};
