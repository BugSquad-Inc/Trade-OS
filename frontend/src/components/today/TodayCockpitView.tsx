import React from 'react';
import { Calendar, CheckCircle2, Clock, ShieldCheck, ArrowRight, TrendingUp, AlertTriangle, Building2, Package, Layers, Sparkles } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';
import { PageSkeleton } from '../ui/PageSkeleton';
import { useTodayCockpit, useCompleteTask } from '../../api/today';
import { useUIStore } from '../../store/uiStore';

export const TodayCockpitView: React.FC = () => {
  const { data: cockpit, isLoading } = useTodayCockpit();
  const completeTask = useCompleteTask();
  const { setCurrentView, setSalesSubTab, setOrdersSubTab, setMoneySubTab, setSelectedBuyerId } = useUIStore();

  if (isLoading) return <PageSkeleton />;

  // Enforce at most 5 priority tasks for the owner
  const rawTasks = cockpit?.urgent_tasks || [];
  const tasks = rawTasks.slice(0, 5);
  const actions = (cockpit?.recommended_actions || []).slice(0, 3);
  const pipeline = cockpit?.pipeline_summary;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Greeting Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-700 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="text-xl font-bold tracking-tight">Today Actions · {cockpit?.exporter_name || "Butler's Leather"}</h2>
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-[11px] font-medium backdrop-blur-md">
              {cockpit?.date || '30 August 2026'}
            </span>
          </div>
          <p className="text-xs text-blue-100 mt-1 max-w-xl font-medium">
            Morning export action briefing for the business owner. Complete the {tasks.length} prioritized actions below to keep shipments on schedule.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-white/15 border border-white/20 text-right backdrop-blur-xs">
            <p className="text-[10px] uppercase font-bold text-blue-100">Export Readiness</p>
            <p className="text-xl font-bold font-mono text-white">{cockpit?.readiness_score || 95}/100</p>
          </div>
        </div>
      </div>

      {/* KPI Highlight Strip with Truth Verification Badges */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <AppleCard variant="default" className="bg-white border-slate-200/90 p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Export Sales</span>
            <TruthStatusBadge status="verified" sourceName="Deal Ledger" checkedDate="Today" showDetails={false} />
          </div>
          <p className="text-2xl font-extrabold font-mono text-slate-900">
            €{(pipeline?.total_pipeline_eur || 182750).toLocaleString()} <span className="text-xs font-normal text-slate-500 font-sans">(₹1.67 Crore)</span>
          </p>
          <p className="text-[11px] text-slate-500 font-medium">
            3 active German buyer contracts in progress
          </p>
        </AppleCard>

        <AppleCard variant="default" className="bg-white border-slate-200/90 p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Pending Action Items</span>
            <AppleBadge tone="orange" size="sm">Top {tasks.length} Focus</AppleBadge>
          </div>
          <p className="text-2xl font-extrabold font-mono text-slate-900">
            {tasks.length} Critical Actions
          </p>
          <p className="text-[11px] text-slate-500 font-medium">
            Sample dispatches, quote sign-offs & eBRC tracking
          </p>
        </AppleCard>

        <AppleCard variant="default" className="bg-white border-slate-200/90 p-4 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Chemical & Forest Rules</span>
            <TruthStatusBadge status="verified" sourceName="TUV Lab Report" checkedDate="28 Aug 2026" showDetails={false} />
          </div>
          <p className="text-2xl font-extrabold font-mono text-emerald-700">
            Export Ready (Grade A)
          </p>
          <p className="text-[11px] text-slate-500 font-medium">
            LWG Gold & REACH test certificates fully valid
          </p>
        </AppleCard>
      </div>

      {/* Urgent Action Tasks Section (Max 5 items) */}
      <div className="space-y-3">
        <div className="flex items-center justify-between px-1">
          <div className="flex items-center gap-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Clock size={14} className="text-amber-500" />
              Prioritized Actions Requiring Sign-Off ({tasks.length})
            </h3>
            <WhatDoesThisMean term="Truth Status Badges" label="How actions are prioritized" />
          </div>

          <button
            onClick={() => setCurrentView('orders')}
            className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
          >
            <span>View Full Orders Pipeline</span>
            <ArrowRight size={13} />
          </button>
        </div>

        <div className="space-y-3">
          {tasks.map((task, idx) => (
            <AppleCard
              key={task.id || idx}
              variant="default"
              className="bg-white border-slate-200/90 shadow-2xs hover:border-blue-300 transition-all p-4 space-y-3"
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="space-y-1 flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-800 text-[10px] font-bold font-mono flex items-center justify-center">
                      {idx + 1}
                    </span>
                    <h4 className="text-sm font-bold text-slate-900">{task.title}</h4>
                    <AppleBadge tone={task.priority === 'urgent' ? 'red' : 'orange'} size="sm">
                      {task.priority}
                    </AppleBadge>
                    <TruthStatusBadge status="verified" sourceName="Workflow Engine" />
                  </div>

                  {task.description && (
                    <p className="text-xs text-slate-600 font-medium pl-7">{task.description}</p>
                  )}

                  <div className="flex items-center gap-3 text-[11px] text-slate-400 pl-7 pt-1">
                    <span>Assigned Owner: <b className="text-slate-700">{task.assigned_to || 'Johann Butler'}</b></span>
                    <span>•</span>
                    <span>Due Date: <b className="text-slate-700">Today, 5:00 PM IST</b></span>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0 w-full sm:w-auto justify-end">
                  <AppleButton
                    variant="primary"
                    size="sm"
                    icon={<CheckCircle2 size={14} />}
                    onClick={() => completeTask.mutate(task.id)}
                  >
                    Mark Done
                  </AppleButton>
                </div>
              </div>
            </AppleCard>
          ))}
        </div>
      </div>

      {/* Recommended High-Velocity Buyer Opportunities */}
      <div className="space-y-3">
        <div className="flex items-center justify-between px-1">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles size={14} className="text-blue-500" />
            Top Recommended Buyer Matches for Butler's Leather
          </h3>
          <WhatDoesThisMean term="HS Code (Harmonized System)" label="How matches are calculated" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {actions.map((act, i) => (
            <AppleCard
              key={i}
              variant="default"
              className="bg-slate-50/70 border-slate-200/80 p-4 space-y-3 flex flex-col justify-between"
            >
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold uppercase text-slate-500 font-mono">
                    {act.type.replace('_', ' ')}
                  </span>
                  <span className="text-xs font-bold font-mono text-emerald-700">
                    €{act.est_deal_value_eur.toLocaleString()} (₹{(act.est_deal_value_eur * 91.5 / 100000).toFixed(1)}L)
                  </span>
                </div>
                <h5 className="text-xs font-bold text-slate-900 leading-snug">{act.title}</h5>
                <p className="text-[11px] text-slate-500">{act.description}</p>
              </div>

              <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between">
                <span className="text-[11px] font-semibold text-slate-700 truncate max-w-[140px]">{act.target}</span>
                <button
                  type="button"
                  onClick={() => {
                    setSelectedBuyerId(act.target);
                    setSalesSubTab('accounts');
                  }}
                  className="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
                >
                  Inspect Buyer <ArrowRight size={12} />
                </button>
              </div>
            </AppleCard>
          ))}
        </div>
      </div>
    </div>
  );
};
