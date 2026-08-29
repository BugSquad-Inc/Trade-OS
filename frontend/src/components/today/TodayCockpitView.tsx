import React from 'react';
import { Calendar, CheckCircle2, Clock, ShieldCheck, ArrowRight, TrendingUp, AlertTriangle, Building2, Package, Layers } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { PageSkeleton } from '../ui/PageSkeleton';
import { useTodayCockpit, useCompleteTask } from '../../api/today';
import { useUIStore } from '../../store/uiStore';

export const TodayCockpitView: React.FC = () => {
  const { data: cockpit, isLoading } = useTodayCockpit();
  const completeTask = useCompleteTask();
  const { setCurrentView } = useUIStore();

  if (isLoading) return <PageSkeleton />;

  const tasks = cockpit?.urgent_tasks || [];
  const actions = cockpit?.recommended_actions || [];
  const pipeline = cockpit?.pipeline_summary;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Greeting Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-700 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="text-xl font-bold tracking-tight">Today Cockpit · {cockpit?.exporter_name}</h2>
            <span className="px-2.5 py-0.5 rounded-full bg-white/20 text-white text-[11px] font-medium backdrop-blur-md">
              {cockpit?.date}
            </span>
          </div>
          <p className="text-xs text-blue-100 mt-1 max-w-xl font-medium">
            Morning export priority briefing. 3 high-impact buyer tasks require your sign-off today.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-white/15 border border-white/20 text-right backdrop-blur-xs">
            <p className="text-[10px] uppercase font-bold text-blue-100">Export Readiness</p>
            <p className="text-xl font-bold font-mono text-white">{cockpit?.readiness_score || 95}/100</p>
          </div>
        </div>
      </div>

      {/* KPI Highlight Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <AppleCard variant="default" className="bg-white border-slate-200/90 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Pipeline</span>
            <AppleBadge tone="blue" size="sm">12 Stages</AppleBadge>
          </div>
          <p className="text-2xl font-extrabold font-mono text-slate-900 mt-1">
            €{(pipeline?.total_pipeline_eur || 182750).toLocaleString()}
          </p>
          <p className="text-[11px] text-slate-500 mt-0.5 font-medium">
            3 active German buyer contracts in flight
          </p>
        </AppleCard>

        <AppleCard variant="default" className="bg-white border-slate-200/90 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Pending Actions</span>
            <AppleBadge tone="orange" size="sm">Urgent</AppleBadge>
          </div>
          <p className="text-2xl font-extrabold font-mono text-slate-900 mt-1">
            {tasks.length} Priority Tasks
          </p>
          <p className="text-[11px] text-slate-500 mt-0.5 font-medium">
            Sample dispatches & quotation follow-ups
          </p>
        </AppleCard>

        <AppleCard variant="default" className="bg-white border-slate-200/90 p-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">EU Compliance Gate</span>
            <AppleBadge tone="green" size="sm">Zero Blockers</AppleBadge>
          </div>
          <p className="text-2xl font-extrabold font-mono text-emerald-700 mt-1">
            Grade A Ready
          </p>
          <p className="text-[11px] text-slate-500 mt-0.5 font-medium">
            LWG Gold & REACH SVHC certificates valid
          </p>
        </AppleCard>
      </div>

      {/* Urgent Action Tasks Section */}
      <div className="space-y-3">
        <div className="flex items-center justify-between px-1">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Clock size={14} className="text-amber-500" />
            Immediate Action Required ({tasks.length})
          </h3>
          <button
            onClick={() => setCurrentView('deals')}
            className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
          >
            <span>View Full Deal Pipeline</span>
            <ArrowRight size={13} />
          </button>
        </div>

        <div className="space-y-3">
          {tasks.map((task) => (
            <AppleCard
              key={task.id}
              variant="default"
              className="bg-white border-slate-200/90 shadow-2xs hover:border-blue-300 transition-all p-4"
            >
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="space-y-1 flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h4 className="text-sm font-bold text-slate-900">{task.title}</h4>
                    <AppleBadge tone={task.priority === 'urgent' ? 'red' : 'orange'} size="sm">
                      {task.priority}
                    </AppleBadge>
                    <span className="text-[11px] font-medium text-slate-400">
                      Assigned: <b className="text-slate-700">{task.assigned_to}</b>
                    </span>
                  </div>
                  {task.description && (
                    <p className="text-xs text-slate-600 font-medium">{task.description}</p>
                  )}
                </div>

                <div className="flex items-center gap-2 shrink-0 w-full sm:w-auto justify-end">
                  <AppleButton
                    variant="primary"
                    size="sm"
                    icon={<CheckCircle2 size={14} />}
                    onClick={() => completeTask.mutate(task.id)}
                  >
                    Done
                  </AppleButton>
                </div>
              </div>
            </AppleCard>
          ))}
        </div>
      </div>

      {/* Recommended Pilot Opportunities */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
          High-Velocity Buyer Opportunities
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {actions.map((act, i) => (
            <AppleCard
              key={i}
              variant="default"
              className="bg-slate-50/70 border-slate-200/80 p-4 space-y-3 flex flex-col justify-between"
            >
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold uppercase text-slate-500 font-mono">{act.type.replace('_', ' ')}</span>
                  <span className="text-xs font-bold font-mono text-emerald-700">€{act.est_deal_value_eur.toLocaleString()}</span>
                </div>
                <h5 className="text-xs font-bold text-slate-900 leading-snug">{act.title}</h5>
                <p className="text-[11px] text-slate-500">{act.description}</p>
              </div>

              <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between">
                <span className="text-[11px] font-semibold text-slate-700">{act.target}</span>
                <button
                  onClick={() => setCurrentView('accounts')}
                  className="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center gap-1 cursor-pointer"
                >
                  Dossier <ArrowRight size={12} />
                </button>
              </div>
            </AppleCard>
          ))}
        </div>
      </div>
    </div>
  );
};
