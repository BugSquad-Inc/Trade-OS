import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/api/client.ts
w("frontend/src/api/client.ts", """const API_KEY = 'tradeos_pilot_secret_key_2026';

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers = {
    'Content-Type': 'application/json',
    'X-TradeOS-Key': API_KEY,
    ...(options.headers || {}),
  };

  const response = await fetch(endpoint, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || `API error: ${response.statusText}`);
  }

  return response.json();
}
""")

# 2. frontend/src/api/capability.ts
w("frontend/src/api/capability.ts", """import { fetchApi } from './client';

export interface ExporterCapability {
  id: string;
  company_name: string;
  location: string;
  cluster: string;
  export_market_focus: string[];
  material_types: string[];
  tannage: string[];
  thickness_range_mm: string[];
  finish_capabilities: string[];
  monthly_capacity_sqft: number;
  moq_sqft: number;
  lead_time_days: number;
  sample_lead_time_days: number;
  port_of_export: string;
  incoterms: string[];
  certifications: string[];
  eudr_readiness_score: number;
  eudr_gap_summary?: string;
}

export const getCapability = () => fetchApi<ExporterCapability>('/api/v1/capability');
""")

# 3. frontend/src/api/matches.ts
w("frontend/src/api/matches.ts", """import { fetchApi } from './client';

export interface DriverItem {
  category: string;
  weight: number;
  score: number;
  title: string;
  evidence: string;
}

export interface MatchCard {
  id: string;
  buyer_id: string;
  name: string;
  legal_name: string;
  country_code: string;
  country: string;
  city: string;
  segment: string;
  rank: number;
  total_score: number;
  grade: string;
  score_breakdown: {
    product_fit: number;
    compliance: number;
    lane_economics: number;
    intent_signals: number;
    accessibility: number;
  };
  drivers: DriverItem[];
  key_gaps: string[];
  next_best_action: string;
  outreach_angle: string;
  status: string;
  contact?: {
    full_name: string;
    title?: string;
    email?: string;
    confidence: number;
    verification_status: string;
  };
  freight_summary: string;
  eudr_readiness_score: number;
}

export interface MatchListResponse {
  matches: MatchCard[];
  total_count: number;
  generated_at: string;
}

export const getMatches = () => fetchApi<MatchListResponse>('/api/v1/matches');
""")

# 4. frontend/src/api/signals.ts
w("frontend/src/api/signals.ts", """import { fetchApi } from './client';

export interface SignalItem {
  id: string;
  entity_id: string;
  company_name: string;
  category: string;
  severity: string;
  title: string;
  summary: string;
  quote?: string;
  source_url?: string;
  detected_at: string;
  score: number;
  evidence: Record<string, any>;
}

export interface EUDRChecklistItem {
  item: string;
  status: string;
  article: string;
  gap_detail?: string;
}

export interface SignalListResponse {
  signals: SignalItem[];
  total_count: number;
  eudr_scorecard: {
    entity: string;
    readiness_score: number;
    status: string;
    requirements: EUDRChecklistItem[];
    top_gap: string;
    recommended_action: string;
  };
  freight_benchmark: {
    origin_port: string;
    destination_port: string;
    mode: string;
    container_type: string;
    rate_usd: number;
    rate_spread: string;
    transit_days: string;
    port_congestion_index: string;
    reroute_risk_notes?: string;
    sample_air_transit: string;
  };
}

export const getSignals = () => fetchApi<SignalListResponse>('/api/v1/signals');
""")

# 5. frontend/src/api/accounts.ts
w("frontend/src/api/accounts.ts", """import { fetchApi } from './client';
import { DriverItem } from './matches';

export interface ContactDetail {
  id: string;
  full_name: string;
  title?: string;
  email?: string;
  phone?: string;
  linkedin_url?: string;
  is_primary: boolean;
  confidence: number;
  verification_status: string;
  consent_status: string;
  legal_basis: string;
}

export interface ProductDetail {
  id: string;
  name: string;
  description?: string;
  hs_code?: string;
  material_types: string[];
  tannage: string[];
  thickness_range_mm: string[];
  finish: string[];
}

export interface Account360 {
  id: string;
  canonical_name: string;
  legal_name?: string;
  domain?: string;
  country_code: string;
  country: string;
  city?: string;
  region?: string;
  website?: string;
  linkedin_url?: string;
  segment: string;
  description?: string;
  founded_year?: number;
  employee_range?: string;
  status: string;
  match_score?: number;
  grade?: string;
  rank?: number;
  drivers: DriverItem[];
  key_gaps: string[];
  next_best_action?: string;
  outreach_angle?: string;
  contacts: ContactDetail[];
  products: ProductDetail[];
  certifications: any[];
  signals: any[];
  eudr_requirements: any[];
  lane_economics: Record<string, any>;
}

export const getAccount360 = (id: string) => fetchApi<Account360>(`/api/v1/accounts/${id}`);

export const generateOutreachApi = (payload: { buyer_id: string; tone: string; contact_name?: string }) =>
  fetchApi<{
    action_id: string;
    buyer_id: string;
    buyer_name: string;
    contact_name: string;
    contact_title: string;
    tone: string;
    subject: string;
    body: string;
    status: string;
  }>('/api/v1/outreach', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
""")

# 6. frontend/src/store/uiStore.ts
w("frontend/src/store/uiStore.ts", """import { create } from 'zustand';

interface UIState {
  currentView: 'matches' | 'signals' | 'accounts';
  selectedBuyerId: string | null;
  selectedInspectorMatch: any | null;
  isCommandBarOpen: boolean;
  isInspectorOpen: boolean;
  setCurrentView: (view: 'matches' | 'signals' | 'accounts') => void;
  setSelectedBuyerId: (id: string | null) => void;
  setSelectedInspectorMatch: (match: any | null) => void;
  setCommandBarOpen: (open: boolean) => void;
  setInspectorOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  currentView: 'matches',
  selectedBuyerId: null,
  selectedInspectorMatch: null,
  isCommandBarOpen: false,
  isInspectorOpen: false,
  setCurrentView: (view) => set({ currentView: view }),
  setSelectedBuyerId: (id) => set({ selectedBuyerId: id }),
  setSelectedInspectorMatch: (match) => set({ selectedInspectorMatch: match, isInspectorOpen: !!match }),
  setCommandBarOpen: (open) => set({ isCommandBarOpen: open }),
  setInspectorOpen: (open) => set({ isInspectorOpen: open }),
}));
""")

# 7. frontend/src/hooks/useMatches.ts
w("frontend/src/hooks/useMatches.ts", """import { useQuery } from '@tanstack/react-query';
import { getMatches } from '../api/matches';

export function useMatches() {
  return useQuery({
    queryKey: ['matches'],
    queryFn: getMatches,
  });
}
""")

# 8. frontend/src/hooks/useSignals.ts
w("frontend/src/hooks/useSignals.ts", """import { useQuery } from '@tanstack/react-query';
import { getSignals } from '../api/signals';

export function useSignals() {
  return useQuery({
    queryKey: ['signals'],
    queryFn: getSignals,
    refetchInterval: 30000,
  });
}
""")

# 9. frontend/src/hooks/useAccount.ts
w("frontend/src/hooks/useAccount.ts", """import { useQuery } from '@tanstack/react-query';
import { getAccount360 } from '../api/accounts';

export function useAccount(id: string | null) {
  return useQuery({
    queryKey: ['account', id],
    queryFn: () => (id ? getAccount360(id) : null),
    enabled: !!id,
  });
}
""")

# 10. frontend/src/hooks/useCapability.ts
w("frontend/src/hooks/useCapability.ts", """import { useQuery } from '@tanstack/react-query';
import { getCapability } from '../api/capability';

export function useCapability() {
  return useQuery({
    queryKey: ['capability'],
    queryFn: getCapability,
  });
}
""")

# 11. frontend/src/components/layout/GlassSidebar.tsx
w("frontend/src/components/layout/GlassSidebar.tsx", """import React from 'react';
import { LayoutGrid, Radio, Building2, ShieldCheck, Ship, ArrowUpRight } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const GlassSidebar: React.FC = () => {
  const { currentView, setCurrentView } = useUIStore();

  const navItems = [
    { id: 'matches', label: 'Match Portal', icon: <LayoutGrid size={18} />, badge: '5 Qualified' },
    { id: 'signals', label: 'Live Signals & EUDR', icon: <Radio size={18} />, badge: 'Live' },
    { id: 'accounts', label: 'Account 360', icon: <Building2 size={18} /> },
  ];

  return (
    <aside className="w-64 glass-sidebar h-screen flex flex-col justify-between p-4 select-none shrink-0">
      <div className="space-y-6">
        {/* App Branding */}
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/25">
            🌍
          </div>
          <div>
            <h1 className="text-sm font-bold text-white tracking-tight flex items-center gap-1.5">
              Trade OS <span className="text-[10px] font-mono px-1.5 py-0.2 bg-blue-500/20 text-blue-300 rounded-full">v1.0</span>
            </h1>
            <p className="text-[11px] text-zinc-400">Export Revenue OS</p>
          </div>
        </div>

        {/* Primary Navigation */}
        <div className="space-y-1">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider px-3 mb-2">Decision Views</p>
          {navItems.map((item) => {
            const active = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setCurrentView(item.id as any)}
                className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl font-medium text-sm transition-all cursor-pointer ${
                  active
                    ? 'bg-blue-600/15 text-blue-300 border border-blue-500/30 shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800/60'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={active ? 'text-blue-400' : 'text-zinc-400'}>{item.icon}</span>
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[10px] px-1.5 py-0.5 rounded-md font-mono ${
                    active ? 'bg-blue-500/30 text-blue-200' : 'bg-zinc-800 text-zinc-400'
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {/* Wedge Corridor Info */}
        <div className="p-3 bg-zinc-900/60 rounded-xl border border-white/[0.06] space-y-2">
          <p className="text-[10px] font-semibold text-zinc-400 uppercase tracking-wider">Active Export Wedge</p>
          <div className="text-xs space-y-1 text-zinc-300">
            <div className="flex items-center justify-between font-medium">
              <span>🇮🇳 Butler's Leather</span>
              <span className="text-zinc-400">Chennai</span>
            </div>
            <div className="flex items-center justify-between text-zinc-400 text-[11px]">
              <span>→ 🇩🇪 German Buyers</span>
              <span>Hamburg</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Metrics */}
      <div className="p-3 bg-emerald-500/10 rounded-xl border border-emerald-500/20 text-xs space-y-1">
        <div className="flex items-center justify-between text-emerald-300 font-semibold">
          <span>Sprint Target</span>
          <span>$500 Pilot</span>
        </div>
        <p className="text-[11px] text-zinc-400">14-Day 5-Qualified-Match Guarantee</p>
      </div>
    </aside>
  );
};
""")

# 12. frontend/src/components/layout/GlassTopbar.tsx
w("frontend/src/components/layout/GlassTopbar.tsx", """import React from 'react';
import { Search, Command, ShieldCheck, Activity } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

export const GlassTopbar: React.FC = () => {
  const { currentView, setCommandBarOpen } = useUIStore();

  const titles = {
    matches: 'Screen 1: Match Portal (Butler\'s Leather → German Buyers)',
    signals: 'Screen 2: Live Trade Signals & EUDR 68/100 Readiness',
    accounts: 'Screen 3: Account 360 Dossier & AI Outreach Cockpit',
  };

  return (
    <header className="h-16 glass-topbar flex items-center justify-between px-6 select-none shrink-0">
      <div>
        <h2 className="text-sm font-semibold text-white tracking-tight">{titles[currentView]}</h2>
        <p className="text-xs text-zinc-400">Leather & Materials Export Intelligence Engine</p>
      </div>

      <div className="flex items-center gap-3">
        {/* Spotlight Command Bar Trigger */}
        <button
          type="button"
          onClick={() => setCommandBarOpen(true)}
          className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-zinc-900/80 border border-white/[0.08] text-xs text-zinc-400 hover:text-zinc-200 hover:border-white/[0.15] transition-all cursor-pointer shadow-sm"
        >
          <Search size={14} />
          <span>Spotlight Search...</span>
          <kbd className="flex items-center gap-0.5 text-[10px] font-mono px-1.5 py-0.5 bg-zinc-800 text-zinc-300 rounded border border-white/[0.06]">
            <Command size={10} /> K
          </kbd>
        </button>

        {/* Live Status Pill */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-medium">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>Live Medallion Sync</span>
        </div>
      </div>
    </header>
  );
};
""")

# 13. frontend/src/components/layout/AppShell.tsx
w("frontend/src/components/layout/AppShell.tsx", """import React from 'react';
import { GlassSidebar } from './GlassSidebar';
import { GlassTopbar } from './GlassTopbar';
import { AppleCommandBar } from '../apple/AppleCommandBar';
import { useUIStore } from '../../store/uiStore';

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const { isCommandBarOpen, setCommandBarOpen, setSelectedBuyerId, setCurrentView } = useUIStore();

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-zinc-950 text-zinc-100">
      {/* Sidebar */}
      <GlassSidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <GlassTopbar />
        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>

      {/* Global Spotlight Palette */}
      <AppleCommandBar
        isOpen={isCommandBarOpen}
        onClose={() => setCommandBarOpen(false)}
        onSelectBuyer={(id) => {
          setSelectedBuyerId(id);
          setCurrentView('accounts');
        }}
        onNavigate={(view) => setCurrentView(view)}
      />
    </div>
  );
};
""")

print("[SUCCESS] Frontend Part 3 (API, Hooks, Layout Shell) built successfully")
