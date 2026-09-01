import React from 'react';
import { LayoutGrid, Radio, Building2, FileText, ArrowRight, ShieldCheck } from 'lucide-react';
import { useUIStore, SalesSubTab } from '../../store/uiStore';
import { MatchPortalView } from '../matches/MatchPortalView';
import { SignalsView } from '../signals/SignalsView';
import { Account360View } from '../accounts/Account360View';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';

export const SalesHubView: React.FC = () => {
  const { salesSubTab, setSalesSubTab, selectedBuyerId, setSelectedBuyerId, openGlossary } = useUIStore();

  const subTabs: { id: SalesSubTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'matches', label: 'Buyer Shortlist', icon: <LayoutGrid size={15} />, badge: '50+ Verified' },
    { id: 'signals', label: 'Market Signals', icon: <Radio size={15} />, badge: 'Live Triggers' },
    { id: 'accounts', label: 'Buyer Outreach & Dossier', icon: <Building2 size={15} /> },
    { id: 'quotes', label: 'Sample Kits & Quotations', icon: <FileText size={15} /> },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header with Sub-Navigation */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-5 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Sales Hub</h2>
              <AppleBadge tone="blue" size="sm">Owner Sales Journey</AppleBadge>
              <TruthStatusBadge status="verified" sourceName="DGFT & Customs Manifest" checkedDate="30 Aug 2026" />
            </div>
            <p className="text-xs text-slate-500 font-medium mt-1">
              Find qualified European buyers, monitor active RFQs and compliance signals, and generate landed-cost quotations.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <WhatDoesThisMean term="HS Code (Harmonized System)" label="Help with Buyer Matching" />
          </div>
        </div>

        {/* Apple HIG Sub-Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto p-1 bg-slate-100/80 rounded-2xl border border-slate-200/60">
          {subTabs.map((tab) => {
            const isActive = salesSubTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setSalesSubTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                  isActive
                    ? 'bg-white text-slate-900 shadow-xs border border-slate-200/80 scale-[1.01]'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                }`}
              >
                <span className={isActive ? 'text-blue-600' : 'text-slate-400'}>{tab.icon}</span>
                <span>{tab.label}</span>
                {tab.badge && (
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-md font-mono ${
                    isActive ? 'bg-blue-100 text-blue-700 font-bold' : 'bg-slate-200 text-slate-600 font-medium'
                  }`}>
                    {tab.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Tab Content Display */}
      {salesSubTab === 'matches' && <MatchPortalView />}
      {salesSubTab === 'signals' && <SignalsView />}
      {salesSubTab === 'accounts' && <Account360View />}
      {salesSubTab === 'quotes' && <SampleAndQuotationsPanel />}
    </div>
  );
};

const SampleAndQuotationsPanel: React.FC = () => {
  const { setSelectedBuyerId, setSalesSubTab } = useUIStore();

  const quotes = [
    {
      id: 'Q-2026-081',
      buyer: 'Bader GmbH & Co. KG',
      country: 'Germany',
      product: 'Automotive Grade Crust Cowhide (1.2-1.4mm)',
      quantity: '30,000 sqft',
      price: '€2.85 / sqft (FOB Chennai)',
      totalEur: 85500,
      marginEst: '18.4%',
      status: 'Awaiting Buyer Review',
      sampleStatus: 'Sample Pack Delivered (DEHAM via DHL Air Express)',
      truth: 'verified'
    },
    {
      id: 'Q-2026-079',
      buyer: 'Roeckl Handschuhe & Accessoires',
      country: 'Germany',
      product: 'Ultra-Supple Goat Nappa (0.6-0.8mm)',
      quantity: '5,000 sqft',
      price: '€3.40 / sqft (CIF Hamburg)',
      totalEur: 17000,
      marginEst: '22.1%',
      status: 'Revision Requested (Thickness Tolerance)',
      sampleStatus: 'Lab Testing Passed (Cr VI < 3ppm)',
      truth: 'verified'
    },
    {
      id: 'Q-2026-074',
      buyer: 'Picard Lederwaren GmbH',
      country: 'Germany',
      product: 'Bovine Full-Grain Classic Nappa (1.1-1.3mm)',
      quantity: '12,000 sqft',
      price: '€3.10 / sqft (FOB Chennai)',
      totalEur: 37200,
      marginEst: '19.8%',
      status: 'Quotation Approved (PO Pending)',
      sampleStatus: 'Swatch Approved by Procurement Lead',
      truth: 'verified'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-slate-900">Active Export Quotations & Sample Tracker</h3>
          <p className="text-xs text-slate-500 font-medium">All quotes are priced with live Chennai-to-Hamburg ocean benchmarks and verified FX rates.</p>
        </div>
        <div className="flex items-center gap-2">
          <WhatDoesThisMean term="Incoterms (FOB, CIF, EXW, DAP)" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {quotes.map((q) => (
          <AppleCard key={q.id} variant="default" className="bg-white border-slate-200 p-5 space-y-4 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono font-bold text-slate-400">{q.id}</span>
                <TruthStatusBadge status={q.truth} sourceName="Cost Model v2.0" />
              </div>
              <h4 className="text-sm font-bold text-slate-900">{q.buyer}</h4>
              <p className="text-xs text-slate-600 font-medium">{q.product}</p>
              
              <div className="p-3 bg-slate-50 rounded-xl space-y-1.5 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-500">Volume:</span>
                  <span className="font-mono font-bold text-slate-800">{q.quantity}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Target Offer:</span>
                  <span className="font-mono font-bold text-slate-800">{q.price}</span>
                </div>
                <div className="flex justify-between border-t border-slate-200/60 pt-1">
                  <span className="text-slate-500">Total Value:</span>
                  <span className="font-mono font-extrabold text-blue-700">€{q.totalEur.toLocaleString()} (₹{(q.totalEur * 91.5 / 100000).toFixed(2)} Lakh)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Est. Margin:</span>
                  <span className="font-mono font-bold text-emerald-700">{q.marginEst}</span>
                </div>
              </div>

              <div className="text-[11px] text-emerald-800 bg-emerald-50/70 p-2 rounded-lg border border-emerald-200/60 font-medium">
                🧪 <b>Sample Status:</b> {q.sampleStatus}
              </div>
            </div>

            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <span className="text-[11px] font-medium text-slate-500">{q.status}</span>
              <AppleButton
                variant="secondary"
                size="sm"
                onClick={() => {
                  setSelectedBuyerId(q.buyer);
                  setSalesSubTab('accounts');
                }}
              >
                Inspect Buyer <ArrowRight size={12} className="ml-1" />
              </AppleButton>
            </div>
          </AppleCard>
        ))}
      </div>
    </div>
  );
};
