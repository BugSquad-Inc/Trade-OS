import React from 'react';

export const PageSkeleton: React.FC = () => (
  <div className="space-y-6 animate-pulse p-6">
    <div className="h-28 bg-slate-200/70 rounded-3xl border border-slate-300/50 shadow-2xs" />
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="h-64 bg-slate-200/60 rounded-3xl border border-slate-300/50 shadow-2xs" />
      <div className="h-64 bg-slate-200/60 rounded-3xl border border-slate-300/50 shadow-2xs" />
      <div className="h-64 bg-slate-200/60 rounded-3xl border border-slate-300/50 shadow-2xs" />
    </div>
  </div>
);
