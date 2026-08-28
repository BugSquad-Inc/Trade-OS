import React from 'react';

interface AppleGaugeProps {
  value: number;
  max?: number;
  label?: string;
  showValue?: boolean;
  tone?: 'green' | 'blue' | 'orange' | 'red';
  className?: string;
}

export const AppleGauge: React.FC<AppleGaugeProps> = ({
  value,
  max = 100,
  label,
  showValue = true,
  tone = 'blue',
  className = '',
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  const colors = {
    green: 'bg-emerald-500',
    blue: 'bg-blue-500',
    orange: 'bg-amber-500',
    red: 'bg-rose-500',
  };

  return (
    <div className={`w-full ${className}`}>
      {(label || showValue) && (
        <div className="flex items-center justify-between text-xs mb-1.5">
          {label && <span className="font-medium text-slate-600">{label}</span>}
          {showValue && <span className="font-mono font-bold text-slate-900">{value}/{max}</span>}
        </div>
      )}
      <div className="h-2 w-full bg-slate-200/80 rounded-full overflow-hidden p-0.5 border border-slate-300/60">
        <div
          className={`h-full rounded-full transition-all duration-500 ease-out ${colors[tone]}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
