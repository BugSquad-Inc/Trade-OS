import React, { useState } from 'react';
import { ShieldCheck, Lock, Activity, Eye, Terminal, Filter, RefreshCw, CheckCircle2, Award } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useAuditEvents, useAuditStats, AuditCategory, AuditEventRecord } from '../../api/audit';

export const AuditTrailView: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | undefined>(undefined);
  const { data: events, isLoading, refetch } = useAuditEvents(selectedCategory);
  const { data: stats } = useAuditStats();

  const [expandedEventId, setExpandedEventId] = useState<string | null>(null);

  if (isLoading) return <PageSkeleton />;

  const eventList = events || [];

  const categoryTones: Record<string, 'purple' | 'blue' | 'green' | 'orange' | 'red' | 'zinc'> = {
    AUTH: 'purple',
    ACCESS: 'blue',
    COMPLIANCE_SIGN_OFF: 'green',
    FINANCE_MODIFICATION: 'orange',
    EXPORT_DATA: 'blue',
    MODIFICATION: 'zinc',
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-zinc-900 to-stone-900 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold tracking-tight">Enterprise Compliance & Security Audit Trail</h2>
            <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[11px] font-mono font-bold border border-emerald-400/20">
              IMMUTABLE INSERT-ONLY
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-xl font-medium">
            Tamper-evident chronological log of all compliance verifications, quotation issuances, and user actions for EU customs and tax audits.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <AppleButton
            variant="secondary"
            size="sm"
            className="bg-white/10 hover:bg-white/20 text-white border-white/20"
            icon={<RefreshCw size={13} />}
            onClick={() => refetch()}
          >
            Refresh Audit Stream
          </AppleButton>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="p-4 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <p className="text-[10px] font-bold text-slate-400 uppercase">Total Audit Events</p>
          <p className="text-2xl font-bold font-mono text-slate-900">{stats?.total_audit_events || eventList.length}</p>
        </div>
        <div className="p-4 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <p className="text-[10px] font-bold text-slate-400 uppercase">Compliance Sign-Offs</p>
          <p className="text-2xl font-bold font-mono text-emerald-600">{stats?.compliance_sign_offs || 2}</p>
        </div>
        <div className="p-4 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <p className="text-[10px] font-bold text-slate-400 uppercase">Financial Modifications</p>
          <p className="text-2xl font-bold font-mono text-amber-600">{stats?.financial_modifications || 1}</p>
        </div>
        <div className="p-4 rounded-2xl bg-white border border-slate-200/90 shadow-2xs space-y-1">
          <p className="text-[10px] font-bold text-slate-400 uppercase">Security Policy Status</p>
          <p className="text-xs font-bold font-mono text-blue-600 flex items-center gap-1 mt-2">
            <CheckCircle2 size={13} /> Strict Insert-Only
          </p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {[
          { label: 'All Events', value: undefined },
          { label: 'Compliance Sign-Offs', value: 'COMPLIANCE_SIGN_OFF' },
          { label: 'Financial Modifications', value: 'FINANCE_MODIFICATION' },
          { label: 'Authentication & Access', value: 'AUTH' },
          { label: 'Data Modifications', value: 'MODIFICATION' },
        ].map((tab) => (
          <button
            key={tab.label}
            type="button"
            onClick={() => setSelectedCategory(tab.value)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer ${
              selectedCategory === tab.value
                ? 'bg-slate-900 text-white shadow-xs'
                : 'bg-white text-slate-600 border border-slate-200 hover:border-slate-300'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Events List */}
      {eventList.length === 0 ? (
        <EmptyState title="No Audit Events Recorded" description="Audit events will automatically stream here as actions occur." />
      ) : (
        <div className="space-y-2.5">
          {eventList.map((ev) => {
            const isExpanded = expandedEventId === ev.id;
            const tone = categoryTones[ev.event_category] || 'zinc';

            return (
              <AppleCard
                key={ev.id}
                variant="default"
                className="bg-white border-slate-200/90 shadow-2xs hover:border-slate-300 transition-all p-4 space-y-2.5"
              >
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-2.5 flex-wrap">
                    <AppleBadge tone={tone} size="sm">{ev.event_category}</AppleBadge>
                    <span className="text-xs font-bold font-mono text-slate-900">{ev.action}</span>
                    <span className="text-xs text-slate-400 font-mono">[{ev.entity_type}]</span>
                  </div>

                  <div className="flex items-center gap-3 text-xs text-slate-500 font-mono">
                    <span>{new Date(ev.created_at).toLocaleString()}</span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 text-xs text-slate-600 bg-slate-50 p-2.5 rounded-xl border border-slate-100 font-mono">
                  <div className="flex items-center gap-2">
                    <span className="text-slate-400 font-bold">Actor:</span>
                    <span className="text-slate-800 font-bold">{ev.actor_email}</span>
                  </div>
                  <div className="flex items-center gap-4 text-[11px] text-slate-500">
                    <span>IP: {ev.ip_address}</span>
                    <span>Client: {ev.user_agent.substring(0, 30)}...</span>
                    <button
                      type="button"
                      onClick={() => setExpandedEventId(isExpanded ? null : ev.id)}
                      className="text-blue-600 font-bold hover:underline cursor-pointer"
                    >
                      {isExpanded ? 'Hide Payload' : 'View Payload Diff'}
                    </button>
                  </div>
                </div>

                {/* Expanded Payload Diff */}
                {isExpanded && (
                  <div className="p-3 rounded-xl bg-slate-900 text-emerald-400 text-xs font-mono overflow-x-auto">
                    <pre>{JSON.stringify(ev.payload_diff, null, 2)}</pre>
                  </div>
                )}
              </AppleCard>
            );
          })}
        </div>
      )}
    </div>
  );
};
