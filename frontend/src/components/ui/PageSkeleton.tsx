import React from 'react';

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
