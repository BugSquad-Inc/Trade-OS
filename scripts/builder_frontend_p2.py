import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/components/apple/AppleSegmentedControl.tsx
w("frontend/src/components/apple/AppleSegmentedControl.tsx", """import React from 'react';
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
    <div className={`inline-flex items-center bg-zinc-900/90 p-1 rounded-xl border border-white/[0.08] relative ${sizeClasses[size]} ${className}`}>
      {options.map((opt) => {
        const isSelected = opt.value === value;
        return (
          <button
            key={opt.value}
            type="button"
            onClick={() => onChange(opt.value)}
            className={`relative z-10 flex items-center justify-center gap-1.5 rounded-lg font-medium transition-colors cursor-pointer select-none ${
              itemSizeClasses[size]
            } ${isSelected ? 'text-white shadow-sm' : 'text-zinc-400 hover:text-zinc-200'}`}
          >
            {isSelected && (
              <motion.div
                layoutId="segmented-pill"
                className="absolute inset-0 bg-zinc-800 rounded-lg shadow-sm border border-white/[0.1] -z-10"
                transition={{ type: 'spring', stiffness: 450, damping: 35 }}
              />
            )}
            {opt.icon && <span className="opacity-90">{opt.icon}</span>}
            <span>{opt.label}</span>
            {opt.count !== undefined && (
              <span className={`text-[11px] px-1.5 py-0.2 rounded-full font-mono ${
                isSelected ? 'bg-blue-500/20 text-blue-300' : 'bg-zinc-800 text-zinc-400'
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
""")

# 2. frontend/src/components/apple/AppleScoreRing.tsx
w("frontend/src/components/apple/AppleScoreRing.tsx", """import React from 'react';
import { motion } from 'framer-motion';

interface AppleScoreRingProps {
  score: number;
  grade?: string;
  size?: number;
  strokeWidth?: number;
  showGrade?: boolean;
  label?: string;
  animate?: boolean;
}

export const AppleScoreRing: React.FC<AppleScoreRingProps> = ({
  score,
  grade,
  size = 72,
  strokeWidth = 6,
  showGrade = true,
  label,
  animate = true,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.min(Math.max(score / 100, 0), 1);
  const strokeDashoffset = circumference - progress * circumference;

  const getColor = (s: number) => {
    if (s >= 85) return '#34C759'; // Apple Green
    if (s >= 70) return '#007AFF'; // Apple Blue
    if (s >= 55) return '#FF9500'; // Apple Orange
    return '#FF3B30';            // Apple Red
  };

  const ringColor = getColor(score);

  return (
    <div className="relative flex flex-col items-center justify-center inline-flex select-none">
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth={strokeWidth}
          fill="none"
        />
        {/* Animated Progress Ring */}
        {animate ? (
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={ringColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ type: 'spring', stiffness: 100, damping: 20 }}
            strokeLinecap="round"
            fill="none"
          />
        ) : (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={ringColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="none"
          />
        )}
      </svg>
      {/* Centered Score Badge */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-base font-bold font-mono tracking-tight text-white leading-none">
          {Math.round(score)}
        </span>
        {showGrade && grade && (
          <span
            className="text-[10px] font-bold px-1.5 py-0.5 rounded-full mt-0.5 leading-none"
            style={{ backgroundColor: `${ringColor}22`, color: ringColor }}
          >
            {grade}
          </span>
        )}
      </div>
      {label && <span className="text-[11px] text-zinc-400 font-medium mt-1">{label}</span>}
    </div>
  );
};
""")

# 3. frontend/src/components/apple/AppleCard.tsx
w("frontend/src/components/apple/AppleCard.tsx", """import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface AppleCardProps extends HTMLMotionProps<'div'> {
  children: React.ReactNode;
  variant?: 'default' | 'inset' | 'elevated' | 'glass';
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export const AppleCard: React.FC<AppleCardProps> = ({
  children,
  variant = 'default',
  className = '',
  onClick,
  hoverable = false,
  ...props
}) => {
  const variantStyles = {
    default: 'bg-zinc-900/70 border border-white/[0.08] backdrop-blur-xl shadow-lg',
    inset: 'bg-zinc-950/60 border border-white/[0.05] shadow-inner',
    elevated: 'bg-zinc-850/90 border border-white/[0.12] shadow-2xl backdrop-blur-2xl',
    glass: 'bg-white/[0.04] border border-white/[0.09] backdrop-blur-md',
  };

  const hoverMotion = hoverable || onClick ? {
    whileHover: { y: -2, transition: { duration: 0.2 } },
    whileTap: { scale: 0.99 },
  } : {};

  return (
    <motion.div
      {...hoverMotion}
      {...props}
      onClick={onClick}
      className={`rounded-2xl p-5 ${variantStyles[variant]} ${onClick ? 'cursor-pointer' : ''} ${className}`}
    >
      {children}
    </motion.div>
  );
};
""")

# 4. frontend/src/components/apple/AppleBadge.tsx
w("frontend/src/components/apple/AppleBadge.tsx", """import React from 'react';

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
""")

# 5. frontend/src/components/apple/AppleButton.tsx
w("frontend/src/components/apple/AppleButton.tsx", """import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface AppleButtonProps extends HTMLMotionProps<'button'> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'glass' | 'danger' | 'subtle';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
  loading?: boolean;
}

export const AppleButton: React.FC<AppleButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  loading = false,
  disabled,
  className = '',
  ...props
}) => {
  const variantStyles = {
    primary: 'bg-blue-600 hover:bg-blue-500 text-white shadow-md shadow-blue-500/20 active:bg-blue-700',
    secondary: 'bg-zinc-800 hover:bg-zinc-750 text-zinc-100 border border-white/[0.08] active:bg-zinc-850',
    glass: 'bg-white/[0.08] hover:bg-white/[0.12] text-white border border-white/[0.12] backdrop-blur-lg active:bg-white/[0.05]',
    danger: 'bg-rose-600 hover:bg-rose-500 text-white shadow-md shadow-rose-500/20 active:bg-rose-700',
    subtle: 'hover:bg-zinc-800/60 text-zinc-400 hover:text-zinc-100 active:bg-zinc-800',
  };

  const sizeStyles = {
    sm: 'text-xs px-3 py-1.5 rounded-lg gap-1.5 font-medium',
    md: 'text-sm px-4 py-2 rounded-xl gap-2 font-medium',
    lg: 'text-base px-5 py-2.5 rounded-xl gap-2.5 font-semibold',
  };

  return (
    <motion.button
      whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center transition-all select-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      {...props}
    >
      {loading ? (
        <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
      ) : (
        icon && <span className="opacity-90">{icon}</span>
      )}
      <span>{children}</span>
    </motion.button>
  );
};
""")

# 6. frontend/src/components/apple/AppleDrawer.tsx
w("frontend/src/components/apple/AppleDrawer.tsx", """import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

interface AppleDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  width?: string;
}

export const AppleDrawer: React.FC<AppleDrawerProps> = ({
  isOpen,
  onClose,
  title,
  subtitle,
  children,
  width = 'max-w-xl',
}) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (isOpen) window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden flex justify-end">
          {/* Backdrop Blur */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm cursor-pointer"
          />

          {/* Slide-over Sheet */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', stiffness: 350, damping: 35 }}
            className={`relative w-full ${width} bg-zinc-900/95 border-l border-white/[0.1] backdrop-blur-2xl shadow-2xl flex flex-col h-full z-10`}
          >
            {/* Drawer Header */}
            <div className="p-6 border-b border-white/[0.08] flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-white tracking-tight">{title}</h3>
                {subtitle && <p className="text-xs text-zinc-400 mt-0.5">{subtitle}</p>}
              </div>
              <button
                type="button"
                onClick={onClose}
                className="p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800/80 transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              {children}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
""")

# 7. frontend/src/components/apple/AppleGauge.tsx
w("frontend/src/components/apple/AppleGauge.tsx", """import React from 'react';

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
          {label && <span className="font-medium text-zinc-400">{label}</span>}
          {showValue && <span className="font-mono font-semibold text-zinc-200">{value}/{max}</span>}
        </div>
      )}
      <div className="h-2 w-full bg-zinc-800 rounded-full overflow-hidden p-0.5 border border-white/[0.05]">
        <div
          className={`h-full rounded-full transition-all duration-500 ease-out ${colors[tone]}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
""")

# 8. frontend/src/components/apple/AppleCommandBar.tsx
w("frontend/src/components/apple/AppleCommandBar.tsx", """import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Building, ShieldCheck, ArrowRight } from 'lucide-react';

interface AppleCommandBarProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectBuyer: (id: string) => void;
  onNavigate: (view: 'matches' | 'signals' | 'accounts') => void;
}

export const AppleCommandBar: React.FC<AppleCommandBarProps> = ({
  isOpen,
  onClose,
  onSelectBuyer,
  onNavigate,
}) => {
  const [query, setQuery] = useState('');

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
        else setQuery('');
      }
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  const mockItems = [
    { type: 'buyer', id: 'picard', title: 'Picard GmbH', subtitle: 'Grade A Match (88/100) · Handbags & Accessories', icon: <Building size={16} /> },
    { type: 'buyer', id: 'roeckl', title: 'Roeckl Handschuhe', subtitle: 'Grade A Match (85/100) · Luxury Gloves & Nappa', icon: <Building size={16} /> },
    { type: 'buyer', id: 'bader', title: 'Bader GmbH & Co. KG', subtitle: 'Grade B Match (82/100) · Automotive Leather', icon: <Building size={16} /> },
    { type: 'screen', id: 'matches', title: 'Match Portal', subtitle: 'View ranked European buyer matches', icon: <ArrowRight size={16} /> },
    { type: 'screen', id: 'signals', title: 'Signals & EUDR Feed', subtitle: 'Review EUDR 68/100 scorecard and freight benchmarks', icon: <ShieldCheck size={16} /> },
  ];

  const filtered = mockItems.filter(i => i.title.toLowerCase().includes(query.toLowerCase()) || i.subtitle.toLowerCase().includes(query.toLowerCase()));

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/70 backdrop-blur-md"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -20 }}
            transition={{ type: 'spring', stiffness: 450, damping: 35 }}
            className="relative w-full max-w-2xl bg-zinc-900/95 border border-white/[0.12] rounded-2xl shadow-2xl backdrop-blur-3xl overflow-hidden z-10"
          >
            {/* Search Input */}
            <div className="flex items-center px-4 py-3.5 border-b border-white/[0.08] gap-3">
              <Search className="text-zinc-400" size={20} />
              <input
                autoFocus
                type="text"
                placeholder="Search German buyers, HS codes, EUDR articles, or signals..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full bg-transparent text-white placeholder-zinc-500 focus:outline-none text-base font-normal"
              />
              <span className="text-[11px] font-mono px-2 py-0.5 bg-zinc-800 text-zinc-400 rounded-md border border-white/[0.06]">
                ESC
              </span>
            </div>

            {/* Results List */}
            <div className="max-h-96 overflow-y-auto p-2 space-y-1">
              {filtered.map((item) => (
                <div
                  key={item.id}
                  onClick={() => {
                    if (item.type === 'screen') onNavigate(item.id as any);
                    else onSelectBuyer(item.id);
                    onClose();
                  }}
                  className="flex items-center justify-between p-3 rounded-xl hover:bg-zinc-800/80 cursor-pointer transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <span className="p-2 rounded-lg bg-zinc-800 text-zinc-300 group-hover:bg-blue-500/20 group-hover:text-blue-300 transition-colors">
                      {item.icon}
                    </span>
                    <div>
                      <h4 className="text-sm font-semibold text-white group-hover:text-blue-200">{item.title}</h4>
                      <p className="text-xs text-zinc-400">{item.subtitle}</p>
                    </div>
                  </div>
                  <span className="text-xs text-zinc-500 group-hover:text-zinc-300 font-medium">Select →</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
""")

# 9. frontend/src/components/ui/PageSkeleton.tsx
w("frontend/src/components/ui/PageSkeleton.tsx", """import React from 'react';

export const PageSkeleton: React.FC = () => (
  <div className="space-y-6 animate-pulse p-6">
    <div className="h-28 bg-zinc-900/80 rounded-2xl border border-white/[0.05]" />
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="h-64 bg-zinc-900/60 rounded-2xl border border-white/[0.05]" />
      <div className="h-64 bg-zinc-900/60 rounded-2xl border border-white/[0.05]" />
      <div className="h-64 bg-zinc-900/60 rounded-2xl border border-white/[0.05]" />
    </div>
  </div>
);
""")

# 10. frontend/src/components/ui/ErrorBoundary.tsx
w("frontend/src/components/ui/ErrorBoundary.tsx", """import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { AppleButton } from '../apple/AppleButton';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[400px] flex flex-col items-center justify-center p-8 text-center bg-zinc-900/50 rounded-2xl border border-rose-500/20 m-6">
          <div className="p-4 bg-rose-500/10 rounded-full text-rose-400 mb-4">
            <AlertTriangle size={32} />
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Something went wrong</h2>
          <p className="text-sm text-zinc-400 max-w-md mb-6">
            {this.state.error?.message || 'An unexpected rendering error occurred in this view.'}
          </p>
          <AppleButton
            variant="secondary"
            icon={<RefreshCw size={16} />}
            onClick={() => this.setState({ hasError: false })}
          >
            Retry Component
          </AppleButton>
        </div>
      );
    }
    return this.props.children;
  }
}
""")

# 11. frontend/src/components/ui/EmptyState.tsx
w("frontend/src/components/ui/EmptyState.tsx", """import React from 'react';
import { Inbox } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
  action?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No items found',
  description = 'Try adjusting your filters or search query to find what you are looking for.',
  action,
}) => (
  <div className="flex flex-col items-center justify-center p-12 text-center bg-zinc-900/40 rounded-2xl border border-white/[0.05]">
    <div className="p-4 bg-zinc-800/80 rounded-full text-zinc-400 mb-3">
      <Inbox size={28} />
    </div>
    <h3 className="text-base font-semibold text-white mb-1">{title}</h3>
    <p className="text-xs text-zinc-400 max-w-sm mb-4">{description}</p>
    {action}
  </div>
);
""")

print("[SUCCESS] Frontend Part 2 (Apple Primitives & UI) built successfully")
