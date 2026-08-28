import React, { useState } from 'react';
import { AccountHeader } from './AccountHeader';
import { OutreachComposer } from './OutreachComposer';
import { AgentCockpitCard } from './AgentCockpitCard';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useAccount } from '../../hooks/useAccount';
import { useMatches } from '../../hooks/useMatches';
import { useUIStore } from '../../store/uiStore';
import { UserCheck, Package, ShieldCheck } from 'lucide-react';

export const Account360View: React.FC = () => {
  const { selectedBuyerId, setSelectedBuyerId } = useUIStore();
  const { data: matchData } = useMatches();

  const effectiveId = selectedBuyerId || matchData?.matches?.[0]?.buyer_id || null;
  const { data: account, isLoading } = useAccount(effectiveId);
  const [activeTab, setActiveTab] = useState<'overview' | 'contacts' | 'outreach' | 'agents'>('outreach');

  if (isLoading) return <PageSkeleton />;
  if (!account) return <EmptyState title="No buyer selected" description="Select a buyer from the Match Portal to inspect their Account 360 dossier." />;

  const primaryContact = account.contacts.find(c => c.is_primary) || account.contacts[0];

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      <AccountHeader account={account} />

      <div className="flex items-center justify-between">
        <AppleSegmentedControl
          size="md"
          value={activeTab}
          onChange={setActiveTab}
          options={[
            { value: 'outreach', label: 'AI Outreach' },
            { value: 'agents', label: 'LangGraph Agents 🤖' },
            { value: 'overview', label: 'Overview & Specs' },
            { value: 'contacts', label: `Contacts (${account.contacts.length})` },
          ]}
        />

        {matchData?.matches && (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-slate-500 font-medium">Switch Buyer:</span>
            <select
              value={effectiveId || ''}
              onChange={(e) => setSelectedBuyerId(e.target.value)}
              className="bg-white border border-slate-200 text-slate-800 rounded-xl px-3 py-1.5 text-xs focus:outline-none focus:border-blue-500 shadow-2xs cursor-pointer font-medium"
            >
              {matchData.matches.map(m => (
                <option key={m.buyer_id} value={m.buyer_id}>
                  #{m.rank} {m.name} ({m.total_score}/100)
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {activeTab === 'outreach' && (
        <OutreachComposer
          buyerId={account.id}
          buyerName={account.canonical_name}
          defaultContact={primaryContact?.full_name}
        />
      )}

      {activeTab === 'agents' && (
        <AgentCockpitCard
          buyerId={account.id}
          buyerName={account.canonical_name}
        />
      )}

      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AppleCard variant="default" className="space-y-3 bg-white">
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Package size={16} className="text-blue-600" /> Sourcing Requirements
            </h4>
            <div className="space-y-2 text-xs">
              {account.products.map(p => (
                <div key={p.id} className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 space-y-1 shadow-2xs">
                  <p className="font-bold text-slate-900">{p.name}</p>
                  <p className="text-slate-500">HS Code: <span className="font-mono text-slate-800 font-semibold">{p.hs_code || '4107'}</span></p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {p.material_types.map((m, i) => (
                      <span key={i} className="px-2 py-0.5 bg-white border border-slate-200 text-slate-700 rounded text-[10px] font-medium shadow-2xs">{m}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </AppleCard>

          <AppleCard variant="default" className="space-y-3 bg-white">
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <ShieldCheck size={16} className="text-emerald-600" /> Compliance & Certifications
            </h4>
            <div className="space-y-2 text-xs">
              {account.certifications.map((c, i) => (
                <div key={i} className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 flex items-center justify-between shadow-2xs">
                  <div>
                    <p className="font-bold text-slate-900">{c.certification_name}</p>
                    <p className="text-[10px] text-slate-500 font-medium">Issuer: {c.issued_by || 'Accredited Lab'}</p>
                  </div>
                  <AppleBadge tone="green" size="sm">Active</AppleBadge>
                </div>
              ))}
            </div>
          </AppleCard>
        </div>
      )}

      {activeTab === 'contacts' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {account.contacts.map(c => (
            <AppleCard key={c.id} variant="default" className="space-y-2 bg-white">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <UserCheck size={16} className="text-emerald-600" />
                  <h4 className="text-sm font-bold text-slate-900">{c.full_name}</h4>
                </div>
                <AppleBadge tone="green" size="sm">Verified ({Math.round(c.confidence * 100)}%)</AppleBadge>
              </div>
              <p className="text-xs text-slate-500 font-medium">{c.title}</p>
              {c.email && <p className="text-xs font-mono text-blue-600 font-semibold pt-1">{c.email}</p>}
              <p className="text-[10px] text-slate-400 pt-1 border-t border-slate-100">{c.legal_basis}</p>
            </AppleCard>
          ))}
        </div>
      )}
    </div>
  );
};
