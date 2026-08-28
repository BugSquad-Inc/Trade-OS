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
    primary: 'bg-blue-600 hover:bg-blue-500 text-white shadow-md shadow-blue-500/20 active:bg-blue-700',
    secondary: 'bg-zinc-800 hover:bg-zinc-700 text-zinc-100 border border-white/[0.08] active:bg-zinc-900',
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
