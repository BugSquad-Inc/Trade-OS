import React from 'react';

export type BadgeTone = 'blue' | 'green' | 'orange' | 'red' | 'purple' | 'indigo' | 'zinc' | 'teal';

interface AppleBadgeProps {
  children: React.ReactNode;
  tone?: BadgeTone;
  size?: 'sm' | 'md';
  icon?: React.ReactNode;
  dot?: boolean;
  className?: string;
}

export const AppleBadge: React.FC<AppleBadgeProps> = ({
  children,
  tone = 'zinc',
  size = 'md',
  icon,
  dot = false,
  className = '',
}) => {
  const toneClasses: Record<BadgeTone, string> = {
    blue: 'bg-blue-50 text-blue-700 border-blue-200/80',
    green: 'bg-emerald-50 text-emerald-700 border-emerald-200/80',
    orange: 'bg-amber-50 text-amber-800 border-amber-200/80',
    red: 'bg-rose-50 text-rose-700 border-rose-200/80',
    purple: 'bg-purple-50 text-purple-700 border-purple-200/80',
    indigo: 'bg-indigo-50 text-indigo-700 border-indigo-200/80',
    teal: 'bg-teal-50 text-teal-700 border-teal-200/80',
    zinc: 'bg-slate-100 text-slate-700 border-slate-200/90',
  };

  const dotColors: Record<BadgeTone, string> = {
    blue: 'bg-blue-500',
    green: 'bg-emerald-500',
    orange: 'bg-amber-500',
    red: 'bg-rose-500',
    purple: 'bg-purple-500',
    indigo: 'bg-indigo-500',
    teal: 'bg-teal-500',
    zinc: 'bg-slate-400',
  };

  const sizeClasses = {
    sm: 'text-[11px] px-2.5 py-0.5 gap-1 font-medium',
    md: 'text-xs px-3 py-1 gap-1.5 font-medium',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full border shadow-2xs ${toneClasses[tone]} ${sizeClasses[size]} ${className}`}
    >
      {dot && <span className={`w-1.5 h-1.5 rounded-full ${dotColors[tone]}`} />}
      {icon && <span className="text-current opacity-80">{icon}</span>}
      <span>{children}</span>
    </span>
  );
};
