import React, { useState } from 'react';
import { ShieldCheck, CheckCircle, XCircle, Clock, AlertCircle, Building2, Filter, Link2, ExternalLink } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useVerificationQueue, useSignOffClaim, useEntityResolutionLinks, VerificationItem } from '../../api/verification';

export const VerificationQueueView: React.FC = () => {
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [selectedItem, setSelectedItem] = useState<VerificationItem | null>(null);
  const [reviewNotes, setReviewNotes] = useState<string>('');

  const { data: queue, isLoading } = useVerificationQueue(statusFilter === 'ALL' ? undefined : statusFilter);
  const { data: resolutionLinks } = useEntityResolutionLinks();
  const signOff = useSignOffClaim();

  if (isLoading) return <PageSkeleton />;

  const queueItems = queue || [];

  const handleSignOff = (approved: boolean) => {
    if (!selectedItem) return;
    signOff.mutate(
      {
        queueId: selectedItem.id,
        approved,
        notes: reviewNotes || (approved ? 'Verified against official registry' : 'Rejected due to insufficient proof'),
      },
      {
        onSuccess: () => {
          setSelectedItem(null);
          setReviewNotes('');
        },
      }
    );
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold tracking-tight">Buyer Verification & Entity Resolution Queue</h2>
            <span className="px-2 py-0.5 rounded-full bg-indigo-500/30 text-indigo-200 text-[11px] font-medium border border-indigo-400/20">
              Analyst Workbench
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-xl font-medium">
            Human-in-the-loop review pipeline. Every European buyer claim requires verified registry, VAT, or official procurement evidence.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1.5 rounded-xl bg-white/10 text-xs font-mono text-white border border-white/10 font-bold">
            Pending Queue: {queueItems.filter((i) => i.status === 'pending' || i.status === 'in_review').length}
          </span>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {['ALL', 'pending', 'in_review', 'verified', 'rejected'].map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all cursor-pointer ${
              statusFilter === st
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200/80'
            }`}
          >
            {st === 'ALL' ? 'All Claims' : st.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Queue List */}
      {queueItems.length === 0 ? (
        <EmptyState
          title="Verification Queue Clear"
          description="All buyer dossiers and trade claims have been audited and signed off."
        />
      ) : (
        <div className="space-y-3">
          {queueItems.map((item) => {
            const isPending = item.status === 'pending' || item.status === 'in_review';
            return (
              <AppleCard
                key={item.id}
                variant="default"
                className="bg-white border-slate-200/90 shadow-2xs hover:border-blue-300 transition-all"
              >
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                  <div className="space-y-1.5 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h4 className="text-sm font-bold text-slate-900">{item.entity_name}</h4>
                      <AppleBadge tone={item.priority === 'high' ? 'red' : 'blue'} size="sm">
                        {item.priority} priority
                      </AppleBadge>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-md font-mono ${
                          item.status === 'verified'
                            ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                            : item.status === 'rejected'
                            ? 'bg-rose-50 text-rose-700 border border-rose-200'
                            : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}
                      >
                        {item.status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 font-medium">
                      Claim: <b className="text-slate-900">{item.claim_type.replace(/_/g, ' ')}</b> · {item.evidence_summary}
                    </p>
                    {item.notes && (
                      <p className="text-[11px] text-slate-500 italic bg-slate-50 p-2 rounded-lg border border-slate-100">
                        "{item.notes}"
                      </p>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 shrink-0 w-full md:w-auto justify-end">
                    {isPending ? (
                      <>
                        <AppleButton
                          variant="secondary"
                          size="sm"
                          onClick={() => setSelectedItem(item)}
                          className="text-rose-600 hover:bg-rose-50 border-rose-200"
                          icon={<XCircle size={13} />}
                        >
                          Reject
                        </AppleButton>
                        <AppleButton
                          variant="primary"
                          size="sm"
                          onClick={() => setSelectedItem(item)}
                          icon={<CheckCircle size={13} />}
                        >
                          Review & Sign Off
                        </AppleButton>
                      </>
                    ) : (
                      <span className="text-xs font-semibold text-slate-400">
                        Audited by: {item.assigned_to}
                      </span>
                    )}
                  </div>
                </div>
              </AppleCard>
            );
          })}
        </div>
      )}

      {/* Review Modal */}
      {selectedItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs" onClick={() => setSelectedItem(null)} />
          <div className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-slate-200 p-6 z-50 space-y-4">
            <div>
              <h3 className="text-base font-bold text-slate-900">Analyst Sign-Off: {selectedItem.entity_name}</h3>
              <p className="text-xs text-slate-500 mt-0.5">Attach registry evidence or rationale for this claim verification.</p>
            </div>

            <div className="space-y-2">
              <label className="block text-xs font-bold text-slate-700">Verification Notes / Register Citation</label>
              <textarea
                rows={3}
                value={reviewNotes}
                onChange={(e) => setReviewNotes(e.target.value)}
                placeholder="e.g. Cross-referenced against German Handelsregister HRB and REACH test reports."
                className="w-full p-3 text-xs rounded-xl bg-slate-50 border border-slate-200 outline-none focus:bg-white focus:border-blue-500 font-medium"
              />
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <AppleButton variant="secondary" size="sm" onClick={() => setSelectedItem(null)}>
                Cancel
              </AppleButton>
              <AppleButton
                variant="secondary"
                size="sm"
                className="text-rose-600 hover:bg-rose-50 border-rose-200"
                onClick={() => handleSignOff(false)}
              >
                Reject Claim
              </AppleButton>
              <AppleButton variant="primary" size="sm" onClick={() => handleSignOff(true)}>
                Verify with Proof
              </AppleButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
