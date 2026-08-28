import React from 'react';
import { motion } from 'framer-motion';

export interface SegmentOption<T extends string> {
  value: T;
  label: string;
  count?: number;
  icon?: React.ReactNode;
}

interface AppleSegmentedControlProps<T extends string> {
  options: SegmentOption<T>[];
  value: T;
  onChange: (value: T) => void;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function AppleSegmentedControl<T extends string>({
  options,
  value,
  onChange,
  size = 'md',
  className = '',
}: AppleSegmentedControlProps<T>) {
  const sizeClasses = {
    sm: 'p-0.5 text-xs',
    md: 'p-1 text-sm',
    lg: 'p-1.5 text-base',
  };

  const itemSizeClasses = {
    sm: 'px-2.5 py-1',
    md: 'px-3.5 py-1.5',
    lg: 'px-4.5 py-2',
  };

  return (
    <div className={`inline-flex items-center bg-slate-200/75 p-1 rounded-xl border border-slate-300/60 shadow-inner relative ${sizeClasses[size]} ${className}`}>
      {options.map((opt) => {
        const isSelected = opt.value === value;
        return (
          <button
            key={opt.value}
            type="button"
            onClick={() => onChange(opt.value)}
            className={`relative z-10 flex items-center justify-center gap-1.5 rounded-lg font-medium transition-colors cursor-pointer select-none ${
              itemSizeClasses[size]
            } ${isSelected ? 'text-slate-900 font-semibold shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
          >
            {isSelected && (
              <motion.div
                layoutId="segmented-pill"
                className="absolute inset-0 bg-white rounded-lg shadow-sm border border-black/[0.04] -z-10"
                transition={{ type: 'spring', stiffness: 450, damping: 35 }}
              />
            )}
            {opt.icon && <span className="opacity-90">{opt.icon}</span>}
            <span>{opt.label}</span>
            {opt.count !== undefined && (
              <span className={`text-[11px] px-1.5 py-0.2 rounded-full font-mono font-semibold ${
                isSelected ? 'bg-blue-100 text-blue-700' : 'bg-slate-300/70 text-slate-700'
              }`}>
                {opt.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
