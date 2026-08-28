import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/api/analytics.ts
w("frontend/src/api/analytics.ts", """import { fetchApi } from './client';

export interface ActivationKPIs {
  profile_completeness_pct: number;
  dossier_completeness_pct: number;
  match_explainability_pct: number;
  verified_contacts_count: number;
}

export interface GTMKPIs {
  total_buyers_monitored: number;
  grade_a_matches: number;
  grade_b_matches: number;
  active_signals_count: number;
  total_customs_teu: number;
  enterprise_mrr_pipeline_usd: number;
}

export interface ExecutiveKPIDashboardResponse {
  timestamp: string;
  active_exporter: string;
  exporter_origin: string;
  activation: ActivationKPIs;
  gtm: GTMKPIs;
  recent_agent_runs: number;
  crm_exports_count: number;
}

export const getExecutiveKPIsApi = () =>
  fetchApi<ExecutiveKPIDashboardResponse>('/api/v1/analytics/kpis');
""")

# 2. frontend/src/components/analytics/ExecutiveDashboardView.tsx
w("frontend/src/components/analytics/ExecutiveDashboardView.tsx", """import React, { useEffect, useState } from 'react';
import { BarChart3, TrendingUp, Users, Target, ShieldCheck, Ship, Bot, CheckCircle2, ArrowUpRight, DollarSign } from 'lucide-react';
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
      <div className="p-6 rounded-3xl bg-gradient-to-r from-emerald-950/40 via-zinc-900/80 to-zinc-900/40 border border-emerald-500/20 backdrop-blur-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-emerald-500/20 text-emerald-400">
                <BarChart3 size={18} />
              </span>
              <h2 className="text-xl font-bold text-white tracking-tight">Executive KPI & Commercial Governance Cockpit</h2>
            </div>
            <p className="text-xs text-zinc-400">
              Active Exporter: <b className="text-white">{data.active_exporter}</b> ({data.exporter_origin}) · Verified Leather & Materials Corridor
            </p>
          </div>

          <div className="flex items-center gap-3">
            <AppleBadge tone="green" size="md">Multi-Tenant Active</AppleBadge>
            <div className="px-3.5 py-1.5 bg-zinc-900 border border-white/[0.08] rounded-xl text-xs font-mono text-zinc-300">
              100% Explainability
            </div>
          </div>
        </div>
      </div>

      {/* Top 4 KPI Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <AppleCard variant="default" className="space-y-2 p-4">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold uppercase">
            <span>Monitored Buyers</span>
            <Target size={14} className="text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-white">{data.gtm.total_buyers_monitored}</div>
          <p className="text-[11px] text-zinc-500">{data.gtm.grade_a_matches} Grade A · {data.gtm.grade_b_matches} Grade B</p>
        </AppleCard>

        <AppleCard variant="default" className="space-y-2 p-4">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold uppercase">
            <span>Verified Contacts</span>
            <Users size={14} className="text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400">{data.activation.verified_contacts_count}</div>
          <p className="text-[11px] text-zinc-500">GDPR Art. 6(1)(f) Compliant</p>
        </AppleCard>

        <AppleCard variant="default" className="space-y-2 p-4">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold uppercase">
            <span>Ocean BOL Volume</span>
            <Ship size={14} className="text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-300">{data.gtm.total_customs_teu} FEU</div>
          <p className="text-[11px] text-zinc-500">INMAA → DEHAM Corridor</p>
        </AppleCard>

        <AppleCard variant="default" className="space-y-2 p-4">
          <div className="flex items-center justify-between text-xs text-zinc-400 font-semibold uppercase">
            <span>Enterprise Pipeline</span>
            <DollarSign size={14} className="text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-300">${data.gtm.enterprise_mrr_pipeline_usd.toLocaleString()}</div>
          <p className="text-[11px] text-zinc-500">Tier: $2,500/month</p>
        </AppleCard>
      </div>

      {/* Activation & Governance Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <AppleCard variant="default" className="space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <CheckCircle2 size={16} className="text-blue-400" /> Activation Health & Readiness
          </h3>
          <div className="space-y-3 text-xs">
            <div>
              <div className="flex justify-between text-zinc-400 mb-1">
                <span>Exporter Profile Completeness</span>
                <span className="font-mono text-white">{data.activation.profile_completeness_pct}%</span>
              </div>
              <div className="w-full bg-zinc-800 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${data.activation.profile_completeness_pct}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-zinc-400 mb-1">
                <span>Buyer Dossier Completeness</span>
                <span className="font-mono text-white">{data.activation.dossier_completeness_pct}%</span>
              </div>
              <div className="w-full bg-zinc-800 rounded-full h-2">
                <div className="bg-emerald-500 h-2 rounded-full" style={{ width: `${data.activation.dossier_completeness_pct}%` }} />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-zinc-400 mb-1">
                <span>100-Point Match Explainability Coverage</span>
                <span className="font-mono text-white">{data.activation.match_explainability_pct}%</span>
              </div>
              <div className="w-full bg-zinc-800 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${data.activation.match_explainability_pct}%` }} />
              </div>
            </div>
          </div>
        </AppleCard>

        <AppleCard variant="default" className="space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Bot size={16} className="text-purple-400" /> Multi-Agent & Audit Activity
          </h3>
          <div className="space-y-2.5 text-xs">
            <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] flex items-center justify-between">
              <div>
                <p className="font-semibold text-white">LangGraph Autonomous Agent Executions</p>
                <p className="text-zinc-500">Research, Compliance & Outreach Agents</p>
              </div>
              <span className="font-mono text-sm font-bold text-purple-300">{data.recent_agent_runs} Runs</span>
            </div>

            <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] flex items-center justify-between">
              <div>
                <p className="font-semibold text-white">Enterprise CRM & Webhook Exports</p>
                <p className="text-zinc-500">HubSpot, Salesforce, CSV</p>
              </div>
              <span className="font-mono text-sm font-bold text-blue-300">{data.crm_exports_count} Dispatches</span>
            </div>

            <div className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] flex items-center justify-between">
              <div>
                <p className="font-semibold text-white">Live Signals Emitted</p>
                <p className="text-zinc-500">Regulatory, Intent, Port Congestion</p>
              </div>
              <span className="font-mono text-sm font-bold text-emerald-300">{data.gtm.active_signals_count} Signals</span>
            </div>
          </div>
        </AppleCard>
      </div>
    </div>
  );
};
""")
