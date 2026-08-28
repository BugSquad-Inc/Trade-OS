import React, { useState } from 'react';
import { AccountHeader } from './AccountHeader';
import { OutreachComposer } from './OutreachComposer';
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
  const [activeTab, setActiveTab] = useState<'overview' | 'contacts' | 'outreach'>('outreach');

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
            { value: 'outreach', label: 'AI Outreach Composer' },
            { value: 'overview', label: 'Company Overview & Specs' },
            { value: 'contacts', label: `Verified Contacts (${account.contacts.length})` },
          ]}
        />

        {matchData?.matches && (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-zinc-500">Switch Buyer:</span>
            <select
              value={effectiveId || ''}
              onChange={(e) => setSelectedBuyerId(e.target.value)}
              className="bg-zinc-900 border border-white/[0.08] text-white rounded-lg px-2.5 py-1 text-xs focus:outline-none"
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

      {activeTab === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <AppleCard variant="default" className="space-y-3">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Package size={16} className="text-blue-400" /> Sourcing Requirements
            </h4>
            <div className="space-y-2 text-xs">
              {account.products.map(p => (
                <div key={p.id} className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] space-y-1">
                  <p className="font-semibold text-white">{p.name}</p>
                  <p className="text-zinc-400">HS Code: <span className="font-mono text-zinc-300">{p.hs_code || '4107'}</span></p>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {p.material_types.map((m, i) => (
                      <span key={i} className="px-2 py-0.5 bg-zinc-800 text-zinc-300 rounded text-[10px]">{m}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </AppleCard>

          <AppleCard variant="default" className="space-y-3">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <ShieldCheck size={16} className="text-emerald-400" /> Compliance & Certifications
            </h4>
            <div className="space-y-2 text-xs">
              {account.certifications.map((c, i) => (
                <div key={i} className="p-3 bg-zinc-950/60 rounded-xl border border-white/[0.05] flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-white">{c.certification_name}</p>
                    <p className="text-[10px] text-zinc-500">Issuer: {c.issued_by || 'Accredited Lab'}</p>
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
            <AppleCard key={c.id} variant="default" className="space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <UserCheck size={16} className="text-emerald-400" />
                  <h4 className="text-sm font-bold text-white">{c.full_name}</h4>
                </div>
                <AppleBadge tone="green" size="sm">Verified ({Math.round(c.confidence * 100)}%)</AppleBadge>
              </div>
              <p className="text-xs text-zinc-400">{c.title}</p>
              {c.email && <p className="text-xs font-mono text-blue-400 pt-1">{c.email}</p>}
              <p className="text-[10px] text-zinc-500 pt-1 border-t border-white/[0.05]">{c.legal_basis}</p>
            </AppleCard>
          ))}
        </div>
      )}
    </div>
  );
};
