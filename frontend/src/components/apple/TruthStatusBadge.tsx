import React from 'react';
import { ShieldCheck, HelpCircle, AlertTriangle, Database, Clock, CheckCircle2, UserCheck } from 'lucide-react';

export type TruthStatus =
  | 'verified'
  | 'declared'
  | 'customer_supplied'
  | 'estimated'
  | 'inferred'
  | 'checked'
  | 'demo'
  | 'stale'
  | 'needs_professional_confirmation'
  | 'disputed';

interface TruthStatusBadgeProps {
  status: TruthStatus | string;
  sourceName?: string;
  checkedDate?: string;
  className?: string;
  showDetails?: boolean;
}

export const TruthStatusBadge: React.FC<TruthStatusBadgeProps> = ({
  status = 'demo',
  sourceName,
  checkedDate,
  className = '',
  showDetails = true,
}) => {
  const getBadgeConfig = () => {
    switch (status) {
      case 'verified':
        return {
          label: 'Verified Claim',
          bg: 'bg-emerald-50 text-emerald-800 border-emerald-300/80',
          dot: 'bg-emerald-500',
          icon: <ShieldCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" />,
        };
      case 'declared':
      case 'customer_supplied':
        return {
          label: 'Exporter Declared',
          bg: 'bg-blue-50 text-blue-800 border-blue-200/80',
          dot: 'bg-blue-500',
          icon: <Database className="w-3.5 h-3.5 text-blue-600 shrink-0" />,
        };
      case 'estimated':
      case 'inferred':
        return {
          label: 'Model Estimated',
          bg: 'bg-purple-50 text-purple-800 border-purple-200/80',
          dot: 'bg-purple-500',
          icon: <HelpCircle className="w-3.5 h-3.5 text-purple-600 shrink-0" />,
        };
      case 'checked':
        return {
          label: 'Rule Checked',
          bg: 'bg-teal-50 text-teal-800 border-teal-200/80',
          dot: 'bg-teal-500',
          icon: <CheckCircle2 className="w-3.5 h-3.5 text-teal-600 shrink-0" />,
        };
      case 'stale':
        return {
          label: 'Review Needed (>90d)',
          bg: 'bg-amber-50 text-amber-800 border-amber-300/80',
          dot: 'bg-amber-500',
          icon: <Clock className="w-3.5 h-3.5 text-amber-600 shrink-0" />,
        };
      case 'needs_professional_confirmation':
        return {
          label: 'Requires CA/CHA Review',
          bg: 'bg-rose-50 text-rose-800 border-rose-300/80',
          dot: 'bg-rose-500',
          icon: <UserCheck className="w-3.5 h-3.5 text-rose-600 shrink-0" />,
        };
      case 'disputed':
        return {
          label: 'Disputed Claim',
          bg: 'bg-red-50 text-red-800 border-red-200/80',
          dot: 'bg-red-500',
          icon: <AlertTriangle className="w-3.5 h-3.5 text-red-600 shrink-0" />,
        };
      case 'demo':
      default:
        return {
          label: 'Sample Record (Demo)',
          bg: 'bg-slate-100 text-slate-700 border-slate-300/80',
          dot: 'bg-slate-400',
          icon: <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />,
        };
    }
  };

  const config = getBadgeConfig();

  return (
    <div
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium border shadow-2xs ${config.bg} ${className}`}
      title={sourceName ? `Source: ${sourceName} ${checkedDate ? `(${checkedDate})` : ''}` : config.label}
    >
      {config.icon}
      <span className="font-semibold">{config.label}</span>
      {showDetails && sourceName && (
        <span className="text-[10px] opacity-75 border-l border-current/20 pl-1.5 ml-0.5 truncate max-w-[130px]">
          {sourceName}
        </span>
      )}
      {showDetails && checkedDate && (
        <span className="text-[9px] opacity-60 font-mono hidden sm:inline">
          • {checkedDate}
        </span>
      )}
    </div>
  );
};
