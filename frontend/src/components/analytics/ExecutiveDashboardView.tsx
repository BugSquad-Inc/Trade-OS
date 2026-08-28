import React, { useEffect, useState } from 'react';
import { BarChart3, Users, Target, Ship, Bot, CheckCircle2, DollarSign } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { PageSkeleton } from '../ui/PageSkeleton';
import { getExecutiveKPIsApi, ExecutiveKPIDashboardResponse } from '../../api/analytics';

export const ExecutiveDashboardView: React.FC = () => {
  const [data, setData] = useState<ExecutiveKPIDashboardResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getExecutiveKPIsApi()
      .then(setData)
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading || !data) return <PageSkeleton />;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-white via-slate-50 to-emerald-50/30 border border-slate-200/90 shadow-sm backdrop-blur-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-emerald-50 text-emerald-600 border border-emerald-200/80 shadow-2xs">
                <BarChart3 size={18} />
              </span>
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Executive KPI & Commercial Governance Cockpit</h2>
            </div>
            <p className="text-xs text-slate-500 font-medium">
              Active Exporter: <b className="text-slate-900">{data.active_exporter}</b> ({data.exporter_origin}) · Verified Leather & Materials Corridor
            </p>
          </div>

          <div className="flex items-center gap-3">
            <AppleBadge tone="green" size="md">Multi-Tenant Active</AppleBadge>
            <div className="px-3.5 py-1.5 bg-white border border-slate-200/90 rounded-xl text-xs font-mono font-semibold text-slate-700 shadow-2xs">
              100% Explainability
            </div>
          </div>
        </div>
      </div>

      {/* Top 4 KPI Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <AppleCard variant="default" className="space-y-2 p-4 bg-white">
          <div className="flex items-center justify-between text-xs text-slate-400 font-bold uppercase tracking-wider">
            <span>Monitored Buyers</span>
            <Target size={14} className="text-blue-600" />
          </div>
          <div className="text-2xl font-bold font-mono text-slate-900">{data.gtm.total_buyers_monitored}</div>
          <p className="text-[11px] text-slate-500 font-medium">{data.gtm.grade_a_matches} Grade A · {data.gtm.grade_b_matches} Grade B</p>
        </AppleCard>

        <AppleCard variant="default" className="space-y-2 p-4 bg-white">
          <div className="flex items-center justify-between text-xs text-slate-400 font-bold uppercase tracking-wider">
            <span>Verified Contacts</span>
            <Users size={14} className="text-emerald-600" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-600">{data.activation.verified_contacts_count}</div>
          <p className="text-[11px] text-slate-500 font-medium">GDPR Art. 6(1)(f) Compliant</p>
        </AppleCard>

        <AppleCard variant="default" className="space-y-2 p-4 bg-white">
          <div className="flex items-center justify-between text-xs text-slate-400 font-bold uppercase tracking-wider">
            <span>Ocean BOL Volume</span>
            <Ship size={14} className="text-purple-600" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-700">{data.gtm.total_customs_teu} FEU</div>
          <p className="text-[11px] text-slate-500 font-medium">INMAA → DEHAM Corridor</p>
        </AppleCard>

        <AppleCard variant="default" className="space-y-2 p-4 bg-white">
          <div className="flex items-center justify-between text-xs text-slate-400 font-bold uppercase tracking-wider">
            <span>Enterprise Pipeline</span>
            <DollarSign size={14} className="text-amber-600" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-700">${data.gtm.enterprise_mrr_pipeline_usd.toLocaleString()}</div>
          <p className="text-[11px] text-slate-500 font-medium">Tier: $2,500/month</p>
        </AppleCard>
      </div>

      {/* Activation & Governance Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <AppleCard variant="default" className="space-y-4 bg-white">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <CheckCircle2 size={16} className="text-blue-600" /> Activation Health & Readiness
          </h3>
          <div className="space-y-3 text-xs">
            <div>
              <div className="flex justify-between text-slate-600 font-medium mb-1">
                <span>Exporter Profile Completeness</span>
                <span className="font-mono text-slate-900 font-bold">{data.activation.profile_completeness_pct}%</span>
              </div>
              <div className="w-full bg-slate-100 border border-slate-200 rounded-full h-2 overflow-hidden">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${data.activation.profile_completeness_pct}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-slate-600 font-medium mb-1">
                <span>Buyer Dossier Completeness</span>
                <span className="font-mono text-slate-900 font-bold">{data.activation.dossier_completeness_pct}%</span>
              </div>
              <div className="w-full bg-slate-100 border border-slate-200 rounded-full h-2 overflow-hidden">
                <div className="bg-emerald-500 h-2 rounded-full" style={{ width: `${data.activation.dossier_completeness_pct}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-slate-600 font-medium mb-1">
                <span>100-Point Match Explainability Coverage</span>
                <span className="font-mono text-slate-900 font-bold">{data.activation.match_explainability_pct}%</span>
              </div>
              <div className="w-full bg-slate-100 border border-slate-200 rounded-full h-2 overflow-hidden">
                <div className="bg-purple-600 h-2 rounded-full" style={{ width: `${data.activation.match_explainability_pct}%` }} />
              </div>
            </div>
          </div>
        </AppleCard>

        <AppleCard variant="default" className="space-y-4 bg-white">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Bot size={16} className="text-purple-600" /> Multi-Agent & Audit Activity
          </h3>
          <div className="space-y-2.5 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-2xl border border-slate-200/80 flex items-center justify-between shadow-2xs">
              <div>
                <p className="font-bold text-slate-900">LangGraph Autonomous Agent Executions</p>
                <p className="text-slate-500 font-medium">Research, Compliance & Outreach Agents</p>
              </div>
              <span className="font-mono text-sm font-bold text-purple-700">{data.recent_agent_runs} Runs</span>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-2xl border border-slate-200/80 flex items-center justify-between shadow-2xs">
              <div>
                <p className="font-bold text-slate-900">Enterprise CRM & Webhook Exports</p>
                <p className="text-slate-500 font-medium">HubSpot, Salesforce, CSV</p>
              </div>
              <span className="font-mono text-sm font-bold text-blue-700">{data.crm_exports_count} Dispatches</span>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-2xl border border-slate-200/80 flex items-center justify-between shadow-2xs">
              <div>
                <p className="font-bold text-slate-900">Live Signals Emitted</p>
                <p className="text-slate-500 font-medium">Regulatory, Intent, Port Congestion</p>
              </div>
              <span className="font-mono text-sm font-bold text-emerald-700">{data.gtm.active_signals_count} Signals</span>
            </div>
          </div>
        </AppleCard>
      </div>
    </div>
  );
};
