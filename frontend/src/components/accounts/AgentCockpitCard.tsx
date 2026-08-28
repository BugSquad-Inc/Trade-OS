import React, { useState } from 'react';
import { Bot, Sparkles, CheckCircle2, ShieldCheck, FileText, Send, Calendar } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { executeAgentsApi, AgentWorkflowResponse } from '../../api/agents';

interface Props {
  buyerId: string;
  buyerName: string;
}

export const AgentCockpitCard: React.FC<Props> = ({ buyerId, buyerName }) => {
  const [isRunning, setIsRunning] = useState(false);
  const [workflow, setWorkflow] = useState<AgentWorkflowResponse | null>(null);

  const handleRunAgents = async () => {
    setIsRunning(true);
    try {
      const res = await executeAgentsApi(buyerId);
      setWorkflow(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <AppleCard variant="default" className="space-y-4 border-purple-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Bot size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">LangGraph Multi-Agent Workflows</h3>
            <p className="text-xs text-zinc-400">Autonomous Research, Compliance, Outreach & 30-Day Plan</p>
          </div>
        </div>

        <AppleButton
          variant="primary"
          size="sm"
          loading={isRunning}
          onClick={handleRunAgents}
          icon={<Sparkles size={14} />}
        >
          {workflow ? 'Re-Run Agent Pack' : 'Run Agent Pack'}
        </AppleButton>
      </div>

      {workflow ? (
        <div className="space-y-4 pt-2">
          {/* Agent Step Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {workflow.completed_steps.map((s, idx) => (
              <div key={idx} className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white flex items-center gap-1.5">
                    <CheckCircle2 size={13} className="text-emerald-400" />
                    {s.agent_name}
                  </span>
                  <span className="text-[10px] font-mono text-zinc-500">{s.execution_time_ms}ms</span>
                </div>
                <p className="text-zinc-400 text-[11px]">
                  {s.agent_name === 'NarrativeAgent' && s.output.narrative}
                  {s.agent_name === 'ComplianceAgent' && `EUDR Score: ${s.output.eudr_readiness_score}/100 — ${s.output.risk_assessment}`}
                  {s.agent_name === 'ResearchAgent' && `Verified: ${s.output.procurement_focus}`}
                  {s.agent_name === 'OutreachSequenceAgent' && `Generated 3-step sequence (Email -> InMail -> Spec)`}
                  {s.agent_name === 'AccountPlanAgent' && `Generated 4-week closing milestones`}
                </p>
              </div>
            ))}
          </div>

          <div className="p-3 bg-purple-500/10 rounded-xl border border-purple-500/20 text-xs text-purple-200 flex items-center justify-between">
            <span className="font-medium">Human-in-the-loop Gate: External communications require user confirmation.</span>
            <AppleBadge tone="purple" size="sm">Gate Active</AppleBadge>
          </div>
        </div>
      ) : (
        <div className="p-6 text-center bg-zinc-950/40 rounded-xl border border-white/[0.05] text-xs text-zinc-400">
          Click <b className="text-white">"Run Agent Pack"</b> to deploy 5 autonomous LangGraph agents for {buyerName}.
        </div>
      )}
    </AppleCard>
  );
};
