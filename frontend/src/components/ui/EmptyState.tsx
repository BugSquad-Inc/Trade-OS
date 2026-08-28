import React from 'react';
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
  <div className="flex flex-col items-center justify-center p-12 text-center bg-white rounded-3xl border border-slate-200/90 shadow-2xs">
    <div className="p-4 bg-slate-100 rounded-2xl text-slate-500 mb-3 shadow-2xs">
      <Inbox size={28} />
    </div>
    <h3 className="text-base font-bold text-slate-900 mb-1">{title}</h3>
    <p className="text-xs text-slate-500 max-w-sm mb-4 font-medium">{description}</p>
    {action}
  </div>
);
