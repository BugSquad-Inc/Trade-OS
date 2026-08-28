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
  <div className="flex flex-col items-center justify-center p-12 text-center bg-zinc-900/40 rounded-2xl border border-white/[0.05]">
    <div className="p-4 bg-zinc-800/80 rounded-full text-zinc-400 mb-3">
      <Inbox size={28} />
    </div>
    <h3 className="text-base font-semibold text-white mb-1">{title}</h3>
    <p className="text-xs text-zinc-400 max-w-sm mb-4">{description}</p>
    {action}
  </div>
);
