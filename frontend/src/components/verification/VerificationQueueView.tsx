import React, { useState } from 'react';
import { ShieldCheck, CheckCircle, XCircle, Clock, AlertCircle, Building2, Filter, Link2, ExternalLink, AlertTriangle, FileText, CheckCircle2, History } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useVerificationQueue, useReviewClaim, useEntityResolutionLinks, VerificationItem } from '../../api/verification';

export const VerificationQueueView: React.FC = () => {
  const [statusFilter, setStatusFilter] = useState<string>('ALL');
  const [selectedItem, setSelectedItem] = useState<VerificationItem | null>(null);
  const [reviewDecision, setReviewDecision] = useState<'approve' | 'reject' | 'dispute'>('approve');
  const [reviewNotes, setReviewNotes] = useState<string>('');
  const [evidenceRef, setEvidenceRef] = useState<string>('');

  const { data: queue, isLoading } = useVerificationQueue(statusFilter === 'ALL' ? undefined : statusFilter);
  const { data: resolutionLinks } = useEntityResolutionLinks();
  const reviewClaim = useReviewClaim();

  if (isLoading) return <PageSkeleton />;

  const queueItems = queue || [];

  const handleExecuteReview = (decision: 'approve' | 'reject' | 'dispute') => {
    if (!selectedItem) return;
    reviewClaim.mutate(
      {
        queueId: selectedItem.id,
        decision,
        notes: reviewNotes || `Analyst decided: ${decision}`,
        evidence_reference: evidenceRef || 'Official Commercial Register',
      },
      {
        onSuccess: () => {
          setSelectedItem(null);
          setReviewNotes('');
          setEvidenceRef('');
        },
      }
    );
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="text-xl font-bold tracking-tight">Analyst Verification & Entity Resolution Queue</h2>
            <span className="px-2 py-0.5 rounded-full bg-indigo-500/30 text-indigo-200 text-[11px] font-medium border border-indigo-400/20">
              Tier A-E Truth Engine
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-xl font-medium">
            Human-in-the-loop review workbench. Verify incoming buyer claims, cross-reference German/EU official registers, and resolve parent-subsidiary corporate entities.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <WhatDoesThisMean term="Truth Status Badges" label="Truth Model Guide" />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {['ALL', 'pending', 'in_review', 'verified', 'rejected', 'disputed'].map((st) => (
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
                className="bg-white border-slate-200/90 shadow-2xs hover:border-blue-300 transition-all p-5"
              >
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                  <div className="space-y-2 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h4 className="text-sm font-bold text-slate-900">{item.entity_name}</h4>
                      <AppleBadge tone={item.priority === 'high' ? 'red' : 'blue'} size="sm">
                        {item.priority} priority
                      </AppleBadge>
                      <TruthStatusBadge status={item.status} sourceName="Analyst Desk" />
                    </div>

                    <p className="text-xs text-slate-600 font-medium">
                      Claim Type: <b className="text-slate-900">{item.claim_type.replace(/_/g, ' ')}</b>
                    </p>

                    {item.evidence_summary && (
                      <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs space-y-1">
                        <span className="text-[10px] font-bold text-slate-400 uppercase">Incoming vs Verified Claim Diff</span>
                        <p className="text-slate-700 font-medium">
                          {item.evidence_summary}
                        </p>
                      </div>
                    )}

                    {item.notes && (
                      <p className="text-[11px] text-slate-500 italic bg-amber-50/60 p-2 rounded-lg border border-amber-200/60">
                        "{item.notes}"
                      </p>
                    )}

                    <div className="text-[10px] text-slate-400 font-mono">
                      Queued: {new Date(item.created_at).toLocaleDateString()} · Assigned: {item.assigned_to || 'Senior Analyst'}
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 shrink-0 w-full md:w-auto justify-end border-t md:border-0 pt-3 md:pt-0 border-slate-100">
                    {isPending ? (
                      <AppleButton
                        variant="primary"
                        size="sm"
                        onClick={() => {
                          setSelectedItem(item);
                          setReviewNotes('');
                          setEvidenceRef('');
                        }}
                        icon={<ShieldCheck size={14} />}
                      >
                        Audit Claim
                      </AppleButton>
                    ) : (
                      <span className="text-xs font-semibold text-slate-500">
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

      {/* Review Modal with Diff View & 3 Decision Options */}
      {selectedItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
          <div className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-slate-200 p-6 space-y-4">
            <div>
              <div className="flex items-center justify-between">
                <h3 className="text-base font-bold text-slate-900">Analyst Claim Review</h3>
                <AppleBadge tone="blue" size="sm">Tier A-E Protocol</AppleBadge>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Target Entity: <b>{selectedItem.entity_name}</b> ({selectedItem.entity_type})
              </p>
            </div>

            {/* Claim Diff Summary */}
            <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200/80 text-xs space-y-1.5">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Incoming Claim vs Registry Record</span>
              <p className="text-slate-800 font-semibold">{selectedItem.claim_type.replace(/_/g, ' ')}</p>
              <p className="text-slate-600">{selectedItem.evidence_summary || 'Verification against Handelsregister HRB and Panjiva bills of lading.'}</p>
            </div>

            {/* Evidence Citation Reference */}
            <div className="space-y-1">
              <label className="block text-xs font-bold text-slate-700">Official Register Reference / Document ID</label>
              <input
                type="text"
                value={evidenceRef}
                onChange={(e) => setEvidenceRef(e.target.value)}
                placeholder="e.g. Handelsregister HRB-712901 / DGFT ICEGATE manifest 2026"
                className="w-full px-3 py-2 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:bg-white font-medium"
              />
            </div>

            {/* Verification Rationale */}
            <div className="space-y-1">
              <label className="block text-xs font-bold text-slate-700">Analyst Verification Notes</label>
              <textarea
                rows={2}
                value={reviewNotes}
                onChange={(e) => setReviewNotes(e.target.value)}
                placeholder="Rationale for verifying or disputing this assertion..."
                className="w-full p-2.5 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:bg-white font-medium"
              />
            </div>

            {/* 3 Decision Actions */}
            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100 flex-wrap">
              <button
                type="button"
                onClick={() => setSelectedItem(null)}
                className="px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
              >
                Cancel
              </button>
              <AppleButton
                variant="secondary"
                size="sm"
                className="text-rose-700 hover:bg-rose-50 border-rose-200"
                onClick={() => handleExecuteReview('reject')}
              >
                Reject
              </AppleButton>
              <AppleButton
                variant="secondary"
                size="sm"
                className="text-amber-700 hover:bg-amber-50 border-amber-200"
                onClick={() => handleExecuteReview('dispute')}
              >
                Flag Dispute
              </AppleButton>
              <AppleButton
                variant="primary"
                size="sm"
                onClick={() => handleExecuteReview('approve')}
              >
                Verify with Evidence
              </AppleButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
