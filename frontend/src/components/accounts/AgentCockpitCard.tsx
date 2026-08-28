import React, { useState } from 'react';
import { Bot, Sparkles, CheckCircle2 } from 'lucide-react';
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
    <AppleCard variant="default" className="space-y-4 border-purple-500/20 bg-white">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-purple-50 text-purple-700 border border-purple-200/80 shadow-2xs">
            <Bot size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 tracking-tight">AI European Export Director</h3>
            <p className="text-xs text-slate-500 font-medium">Automated Buyer Research, EUDR Compliance Pack, Sample Pitch & 30-Day Deal Plan</p>
          </div>
        </div>

        <AppleButton
          variant="primary"
          size="sm"
          loading={isRunning}
          onClick={handleRunAgents}
          icon={<Sparkles size={14} />}
        >
          {workflow ? 'Regenerate Deal Pack' : 'Generate 30-Day Deal Pack'}
        </AppleButton>
      </div>

      {workflow ? (
        <div className="space-y-4 pt-2">
          {/* Agent Step Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {workflow.completed_steps.map((s, idx) => (
              <div key={idx} className="p-3 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-1 shadow-2xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 flex items-center gap-1.5">
                    <CheckCircle2 size={13} className="text-emerald-600" />
                    {s.agent_name}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400 font-semibold">{s.execution_time_ms}ms</span>
                </div>
                <p className="text-slate-600 text-[11px] leading-relaxed">
                  {s.agent_name === 'NarrativeAgent' && s.output.narrative}
                  {s.agent_name === 'ComplianceAgent' && `EUDR Score: ${s.output.eudr_readiness_score}/100 — ${s.output.risk_assessment}`}
                  {s.agent_name === 'ResearchAgent' && `Verified: ${s.output.procurement_focus}`}
                  {s.agent_name === 'OutreachSequenceAgent' && `Generated 3-step sequence (Email -> InMail -> Spec)`}
                  {s.agent_name === 'AccountPlanAgent' && `Generated 4-week closing milestones`}
                </p>
              </div>
            ))}
          </div>

          <div className="p-3 bg-purple-50 rounded-xl border border-purple-200 text-xs text-purple-900 flex items-center justify-between shadow-2xs">
            <span className="font-semibold">Human-in-the-loop Gate: External communications require user confirmation.</span>
            <AppleBadge tone="purple" size="sm">Gate Active</AppleBadge>
          </div>
        </div>
      ) : (
        <div className="p-8 text-center bg-slate-50 rounded-2xl border border-slate-200/80 text-xs text-slate-500 font-medium">
          Click <b className="text-slate-900 font-bold">"Run Agent Pack"</b> to deploy 5 autonomous LangGraph agents for {buyerName}.
        </div>
      )}
    </AppleCard>
  );
};
