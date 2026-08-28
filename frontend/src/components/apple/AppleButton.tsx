import React from 'react';
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
    primary: 'bg-[#007AFF] hover:bg-[#0071E3] text-white shadow-sm shadow-blue-500/20 active:bg-blue-700 font-semibold',
    secondary: 'bg-white hover:bg-slate-50 text-slate-800 border border-slate-200/90 shadow-2xs active:bg-slate-100 font-medium',
    glass: 'bg-white/80 hover:bg-white text-slate-800 border border-slate-200/80 shadow-2xs backdrop-blur-md active:bg-slate-50 font-medium',
    danger: 'bg-rose-600 hover:bg-rose-500 text-white shadow-sm shadow-rose-500/20 active:bg-rose-700 font-semibold',
    subtle: 'hover:bg-slate-200/60 text-slate-600 hover:text-slate-900 active:bg-slate-200 font-medium',
  };

  const sizeStyles = {
    sm: 'text-xs px-3 py-1.5 rounded-lg gap-1.5',
    md: 'text-sm px-4 py-2 rounded-xl gap-2',
    lg: 'text-base px-5 py-2.5 rounded-xl gap-2.5',
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
