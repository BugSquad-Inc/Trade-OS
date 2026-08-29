import React from 'react';
import { ShieldCheck, HelpCircle, AlertTriangle, Database, Clock } from 'lucide-react';

export type TruthStatus =
  | 'verified'
  | 'inferred'
  | 'customer_supplied'
  | 'provider_supplied'
  | 'demo'
  | 'stale'
  | 'disputed'
  | 'unavailable';

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
  showDetails = false,
}) => {
  const getBadgeConfig = () => {
    switch (status) {
      case 'verified':
        return {
          label: 'Verified Claim',
          bg: 'bg-emerald-50 text-emerald-700 border-emerald-200/80',
          dot: 'bg-emerald-500',
          icon: <ShieldCheck className="w-3 h-3 text-emerald-600" />,
        };
      case 'inferred':
        return {
          label: 'Inferred Signal',
          bg: 'bg-indigo-50 text-indigo-700 border-indigo-200/80',
          dot: 'bg-indigo-500',
          icon: <HelpCircle className="w-3 h-3 text-indigo-600" />,
        };
      case 'customer_supplied':
        return {
          label: 'Exporter Declared',
          bg: 'bg-blue-50 text-blue-700 border-blue-200/80',
          dot: 'bg-blue-500',
          icon: <Database className="w-3 h-3 text-blue-600" />,
        };
      case 'stale':
        return {
          label: 'Review Needed (>90d)',
          bg: 'bg-amber-50 text-amber-700 border-amber-200/80',
          dot: 'bg-amber-500',
          icon: <Clock className="w-3 h-3 text-amber-600" />,
        };
      case 'disputed':
        return {
          label: 'Disputed Claim',
          bg: 'bg-red-50 text-red-700 border-red-200/80',
          dot: 'bg-red-500',
          icon: <AlertTriangle className="w-3 h-3 text-red-600" />,
        };
      case 'demo':
      default:
        return {
          label: 'Sample Record (Demo)',
          bg: 'bg-amber-50/80 text-amber-700 border-amber-300/70',
          dot: 'bg-amber-400',
          icon: <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />,
        };
    }
  };

  const config = getBadgeConfig();

  return (
    <div className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-medium border ${config.bg} ${className}`}>
      {config.icon}
      <span>{config.label}</span>
      {showDetails && sourceName && (
        <span className="text-[10px] opacity-75 border-l border-current/20 pl-1.5 ml-0.5">
          {sourceName}
        </span>
      )}
      {showDetails && checkedDate && (
        <span className="text-[9px] opacity-60">
          • {checkedDate}
        </span>
      )}
    </div>
  );
};
