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
    default: 'bg-zinc-900/70 border border-white/[0.08] backdrop-blur-xl shadow-lg',
    inset: 'bg-zinc-950/60 border border-white/[0.05] shadow-inner',
    elevated: 'bg-zinc-800/90 border border-white/[0.12] shadow-2xl backdrop-blur-2xl',
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
