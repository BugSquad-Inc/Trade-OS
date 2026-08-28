import React from 'react';
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
