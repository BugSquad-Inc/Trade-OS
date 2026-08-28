import React from 'react';
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
    default: 'bg-white/85 border border-slate-200/80 backdrop-blur-xl shadow-[0_4px_20px_rgba(0,0,0,0.03)] hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)]',
    inset: 'bg-slate-100/75 border border-slate-200/70 shadow-inner',
    elevated: 'bg-white/95 border border-slate-200/90 shadow-[0_12px_40px_rgba(0,0,0,0.08)] backdrop-blur-2xl',
    glass: 'bg-white/60 border border-slate-200/60 backdrop-blur-md shadow-sm',
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
