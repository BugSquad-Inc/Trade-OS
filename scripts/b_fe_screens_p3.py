import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/components/accounts/AccountHeader.tsx
w("frontend/src/components/accounts/AccountHeader.tsx", """import React from 'react';
import { MapPin } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleScoreRing } from '../apple/AppleScoreRing';
import { Account360 } from '../../api/accounts';

interface Props {
  account: Account360;
}

export const AccountHeader: React.FC<Props> = ({ account }) => {
  return (
    <AppleCard variant="default" className="space-y-4 border-blue-500/20">
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <div className="p-3 rounded-2xl bg-zinc-800 text-white font-bold text-xl border border-white/[0.08]">
              {account.rank ? `#${account.rank}` : '🇩🇪'}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-2xl font-bold text-white tracking-tight">{account.canonical_name}</h2>
                {account.grade && <AppleBadge tone="green" size="sm">Grade {account.grade} Fit</AppleBadge>}
              </div>
              <p className="text-xs text-zinc-400 flex items-center gap-2 mt-0.5">
                <MapPin size={13} className="text-zinc-500" />
                <span>{account.city}, {account.country}</span> · <span className="text-zinc-300 font-medium">{account.segment}</span>
              </p>
            </div>
          </div>

          <p className="text-xs text-zinc-300 max-w-2xl leading-relaxed">{account.description}</p>
        </div>

        {account.match_score && (
          <div className="shrink-0 flex items-center gap-4 p-4 rounded-xl bg-zinc-950/60 border border-white/[0.08]">
            <div className="text-right">
              <span className="text-xs font-semibold text-zinc-400 uppercase">Match Score</span>
              <p className="text-2xl font-bold font-mono text-white">{account.match_score}<span className="text-xs text-zinc-500">/100</span></p>
            </div>
            <AppleScoreRing score={account.match_score} grade={account.grade} size={58} strokeWidth={5} />
          </div>
        )}
      </div>
    </AppleCard>
  );
};
""")

# 2. frontend/src/components/accounts/OutreachComposer.tsx
w("frontend/src/components/accounts/OutreachComposer.tsx", """import React, { useState } from 'react';
import { Sparkles, Copy, Check, Send, AlertCircle } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';
import { generateOutreachApi } from '../../api/accounts';

interface Props {
  buyerId: string;
  buyerName: string;
  defaultContact?: string;
}

export const OutreachComposer: React.FC<Props> = ({ buyerId, buyerName, defaultContact }) => {
  const [tone, setTone] = useState<'Professional' | 'Direct' | 'Technical' | 'Relationship'>('Professional');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async (selectedTone = tone) => {
    setIsGenerating(true);
    try {
      const res = await generateOutreachApi({
        buyer_id: buyerId,
        tone: selectedTone,
        contact_name: defaultContact,
      });
      setSubject(res.subject);
      setBody(res.body);
    } catch (e: any) {
      console.error(e);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(`Subject: ${subject}\n\n${body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <AppleCard variant="default" className="space-y-4 border-indigo-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Sparkles size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">AI Export Outreach Composer</h3>
            <p className="text-xs text-zinc-400">Personalized to {buyerName} with EUDR & Freight Context</p>
          </div>
        </div>

        <AppleButton
          variant="primary"
          size="sm"
          loading={isGenerating}
          onClick={() => handleGenerate()}
          icon={<Sparkles size={14} />}
        >
          Generate Message
        </AppleButton>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-zinc-400 font-semibold uppercase tracking-wider">Outreach Tone:</span>
        <AppleSegmentedControl
          size="sm"
          value={tone}
          onChange={(newTone: any) => {
            setTone(newTone);
            handleGenerate(newTone);
          }}
          options={[
            { value: 'Professional', label: 'Professional' },
            { value: 'Direct', label: 'Direct & Concise' },
            { value: 'Technical', label: 'Technical Spec' },
            { value: 'Relationship', label: 'Relationship' },
          ]}
        />
      </div>

      <div className="p-2.5 bg-zinc-950/60 rounded-xl border border-white/[0.06] text-[11px] text-zinc-400 flex items-center gap-2">
        <AlertCircle size={14} className="text-zinc-500 shrink-0" />
        <span>Contact roles sourced from public directories under GDPR Art. 6(1)(f) Legitimate Interest — verify before outreach.</span>
      </div>

      {body ? (
        <div className="space-y-3 pt-2">
          <div>
            <label className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">Subject Line</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full mt-1 p-2.5 rounded-xl bg-zinc-950/80 border border-white/[0.08] text-sm text-white font-medium focus:outline-none focus:border-blue-500/50"
            />
          </div>

          <div>
            <label className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">Email Body</label>
            <textarea
              rows={10}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full mt-1 p-3 rounded-xl bg-zinc-950/80 border border-white/[0.08] text-xs text-zinc-200 leading-relaxed font-sans focus:outline-none focus:border-blue-500/50 font-mono"
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <AppleButton
              variant="secondary"
              size="sm"
              onClick={handleCopy}
              icon={copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
            >
              {copied ? 'Copied to Clipboard' : 'Copy Message'}
            </AppleButton>

            <AppleButton
              variant="glass"
              size="sm"
              onClick={() => window.open(`mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`)}
              icon={<Send size={14} />}
            >
              Open in Mail App
            </AppleButton>
          </div>
        </div>
      ) : (
        <div className="p-8 text-center bg-zinc-950/40 rounded-xl border border-white/[0.05] text-xs text-zinc-400">
          Click <b className="text-white">"Generate Message"</b> to draft a personalized outreach email for {buyerName}.
        </div>
      )}
    </AppleCard>
  );
};
""")

# 3. frontend/src/components/accounts/Account360View.tsx
w("frontend/src/components/accounts/Account360View.tsx", """import React, { useState } from 'react';
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
""")

# 4. frontend/src/App.tsx
w("frontend/src/App.tsx", """import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/layout/AppShell';
import { MatchPortalView } from './components/matches/MatchPortalView';
import { SignalsView } from './components/signals/SignalsView';
import { Account360View } from './components/accounts/Account360View';
import { ErrorBoundary } from './components/ui/ErrorBoundary';
import { useUIStore } from './store/uiStore';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      refetchOnWindowFocus: false,
    },
  },
});

function AppContent() {
  const { currentView } = useUIStore();

  return (
    <AppShell>
      <ErrorBoundary>
        {currentView === 'matches' && <MatchPortalView />}
        {currentView === 'signals' && <SignalsView />}
        {currentView === 'accounts' && <Account360View />}
      </ErrorBoundary>
    </AppShell>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}
""")

# 5. frontend/src/main.tsx
w("frontend/src/main.tsx", """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

print("[SUCCESS] Screen 3 (Account 360 & App Entry) built successfully")
