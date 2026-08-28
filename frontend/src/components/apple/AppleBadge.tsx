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
    blue: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
    green: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    orange: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    red: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    purple: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
    indigo: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30',
    teal: 'bg-teal-500/15 text-teal-300 border-teal-500/30',
    zinc: 'bg-zinc-800/80 text-zinc-300 border-white/[0.08]',
  };

  const dotColors: Record<BadgeTone, string> = {
    blue: 'bg-blue-400',
    green: 'bg-emerald-400',
    orange: 'bg-amber-400',
    red: 'bg-rose-400',
    purple: 'bg-purple-400',
    indigo: 'bg-indigo-400',
    teal: 'bg-teal-400',
    zinc: 'bg-zinc-400',
  };

  const sizeClasses = {
    sm: 'text-[11px] px-2 py-0.5 gap-1',
    md: 'text-xs px-2.5 py-1 gap-1.5',
  };

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full border ${toneClasses[tone]} ${sizeClasses[size]} ${className}`}
    >
      {dot && <span className={`w-1.5 h-1.5 rounded-full ${dotColors[tone]}`} />}
      {icon && <span className="text-current opacity-80">{icon}</span>}
      <span>{children}</span>
    </span>
  );
};
