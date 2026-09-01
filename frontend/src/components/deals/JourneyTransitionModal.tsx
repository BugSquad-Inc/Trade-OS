import React, { useState } from 'react';
import { X, CheckCircle2, AlertTriangle, ShieldCheck, Clock, ArrowRight, FileText, UserCheck, Lock } from 'lucide-react';
import { useJourneyState, useExecuteTransition, JourneyActionDefinition, BlockedActionDefinition } from '../../api/journey';
import { Opportunity } from '../../api/deals';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';

interface JourneyTransitionModalProps {
  opportunity: Opportunity | null;
  isOpen: boolean;
  onClose: () => void;
}

export const JourneyTransitionModal: React.FC<JourneyTransitionModalProps> = ({
  opportunity,
  isOpen,
  onClose,
}) => {
  const oppId = opportunity?.id;
  const { data: journeyState, isLoading } = useJourneyState(oppId);
  const executeTransition = useExecuteTransition();

  const [selectedAction, setSelectedAction] = useState<JourneyActionDefinition | null>(null);
  const [evidenceNote, setEvidenceNote] = useState('');
  const [reasonCode, setReasonCode] = useState('owner_decision');

  if (!isOpen || !opportunity) return null;

  const handleExecute = (action: JourneyActionDefinition) => {
    executeTransition.mutate(
      {
        oppId: opportunity.id,
        req: {
          action_id: action.action_id,
          actor: 'Johann Butler (Owner)',
          actor_role: action.required_role || 'owner',
          reason_code: reasonCode,
          notes: evidenceNote || `Executed action: ${action.label}`,
          evidence_references: evidenceNote ? { note: evidenceNote } : {},
          idempotency_key: `trans-${opportunity.id}-${action.action_id}-${Date.now()}`,
        },
      },
      {
        onSuccess: () => {
          setSelectedAction(null);
          setEvidenceNote('');
          onClose();
        },
      }
    );
  };

  const availableActions = journeyState?.available_actions || [];
  const blockedActions = journeyState?.blocked_actions || [];
  const history = journeyState?.history || [];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="relative w-full max-w-2xl max-h-[85vh] bg-white rounded-3xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200/80 bg-slate-50/80 shrink-0">
          <div className="space-y-0.5">
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-slate-900 tracking-tight">
                Export Journey Stage Gate
              </h2>
              <AppleBadge tone="blue" size="sm">Backend Governed</AppleBadge>
            </div>
            <p className="text-xs text-slate-500 font-medium truncate max-w-lg">
              {opportunity.title} · {opportunity.buyer?.legal_name || 'Buyer'}
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">
          {/* Current State Card */}
          <div className="p-4 bg-blue-50/60 rounded-2xl border border-blue-100 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold uppercase tracking-wider text-blue-800 font-mono">
                Current Macro Stage: {journeyState?.macro_stage?.replace(/_/g, ' ').toUpperCase() || 'FIND BUYERS'}
              </span>
              <TruthStatusBadge status="verified" sourceName="Stage Engine" checkedDate="Live" />
            </div>

            <h3 className="text-base font-bold text-slate-900">
              {journeyState?.stage_title || opportunity.stage.replace(/_/g, ' ').toUpperCase()}
            </h3>

            <p className="text-xs text-slate-700 font-medium">
              🧭 <b>Owner Decision Gate:</b> {journeyState?.owner_question || 'What is the required next business action?'}
            </p>
          </div>

          {/* Available Actions Section */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <CheckCircle2 size={14} className="text-emerald-600" />
              Permitted Next Actions ({availableActions.length})
            </h4>

            {availableActions.length === 0 ? (
              <p className="text-xs text-slate-500 italic p-3 bg-slate-50 rounded-xl">
                No active forward transitions available for this stage.
              </p>
            ) : (
              <div className="space-y-2">
                {availableActions.map((act) => (
                  <div
                    key={act.action_id}
                    className="p-3.5 rounded-2xl bg-white border border-slate-200 hover:border-blue-400 transition-all space-y-2 shadow-2xs"
                  >
                    <div className="flex items-center justify-between gap-3">
                      <div>
                        <h5 className="text-sm font-bold text-slate-900">{act.label}</h5>
                        <p className="text-xs text-slate-500 font-medium">{act.description}</p>
                      </div>

                      <AppleButton
                        variant={act.action_id === 'close_lost' ? 'secondary' : 'primary'}
                        size="sm"
                        disabled={executeTransition.isPending}
                        onClick={() => {
                          if (act.requires_evidence) {
                            setSelectedAction(act);
                          } else {
                            handleExecute(act);
                          }
                        }}
                      >
                        {act.requires_evidence ? 'Review & Submit' : 'Advance'}
                      </AppleButton>
                    </div>

                    <div className="flex items-center gap-3 text-[10px] text-slate-400 font-medium pt-1 border-t border-slate-100">
                      <span>Target Stage: <b className="text-slate-700">{act.target_stage.replace(/_/g, ' ')}</b></span>
                      <span>•</span>
                      <span>Required Role: <b className="text-slate-700">{act.required_role}</b></span>
                      {act.requires_evidence && (
                        <>
                          <span>•</span>
                          <span className="text-amber-700 font-bold">Evidence Required</span>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Evidence Prompt Modal (if action requires evidence) */}
          {selectedAction && (
            <div className="p-4 bg-amber-50/70 border border-amber-200/80 rounded-2xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-amber-950 flex items-center gap-1.5">
                  <AlertTriangle size={14} className="text-amber-600" />
                  Prerequisite & Evidence Required for "{selectedAction.label}"
                </span>
                <button
                  type="button"
                  onClick={() => setSelectedAction(null)}
                  className="text-xs text-slate-400 hover:text-slate-700"
                >
                  Cancel
                </button>
              </div>

              <p className="text-xs text-amber-900">
                {selectedAction.evidence_prompt || 'Please provide verification reference, PO number, or note.'}
              </p>

              <input
                type="text"
                placeholder="Enter document reference number, PO ID, or decision reason..."
                value={evidenceNote}
                onChange={(e) => setEvidenceNote(e.target.value)}
                className="w-full px-3 py-2 text-xs rounded-xl bg-white border border-amber-300 focus:outline-hidden focus:ring-2 focus:ring-amber-500/20 font-medium"
              />

              <div className="flex justify-end gap-2 pt-1">
                <AppleButton
                  variant="primary"
                  size="sm"
                  disabled={!evidenceNote.trim() || executeTransition.isPending}
                  onClick={() => handleExecute(selectedAction)}
                >
                  Submit Stage Transition
                </AppleButton>
              </div>
            </div>
          )}

          {/* Blocked Actions Section */}
          {blockedActions.length > 0 && (
            <div className="space-y-3 pt-2">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Lock size={14} className="text-slate-400" />
                Blocked Actions ({blockedActions.length})
              </h4>

              <div className="space-y-2">
                {blockedActions.map((b) => (
                  <div key={b.action_id} className="p-3 bg-slate-50 rounded-2xl border border-slate-200/60 text-xs space-y-1 opacity-80">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-700">{b.label}</span>
                      <AppleBadge tone="zinc" size="sm">Blocked</AppleBadge>
                    </div>
                    {b.blocked_reasons.map((r, i) => (
                      <p key={i} className="text-[11px] text-slate-500">❌ {r}</p>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Chronological Audit Event History */}
          <div className="space-y-3 pt-2 border-t border-slate-100">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Clock size={14} className="text-slate-400" />
              Immutable Stage Transition History ({history.length})
            </h4>

            {history.length === 0 ? (
              <p className="text-xs text-slate-400 italic">No transition events logged yet.</p>
            ) : (
              <div className="space-y-2">
                {history.map((ev) => (
                  <div key={ev.id} className="p-3 bg-slate-50/70 rounded-xl border border-slate-200/60 text-xs space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-900">{ev.action}</span>
                      <span className="text-[10px] font-mono text-slate-400">{new Date(ev.created_at).toLocaleString()}</span>
                    </div>
                    <p className="text-[11px] text-slate-600">
                      Actor: <b>{ev.actor}</b> ({ev.actor_role}) · Previous: {ev.previous_stage} → New: <b>{ev.new_stage}</b>
                    </p>
                    {ev.notes && <p className="text-[10px] text-slate-500 italic">"{ev.notes}"</p>}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex items-center justify-between shrink-0">
          <span>Backend Authority: journey_service.py • Strictly Audited</span>
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1 bg-slate-200 hover:bg-slate-300 rounded-lg text-slate-700 font-bold transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
