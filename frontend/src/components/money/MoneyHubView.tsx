import React from 'react';
import { DollarSign, CheckCircle2, TrendingUp, BarChart3, AlertCircle, FileCheck, ArrowRight } from 'lucide-react';
import { useUIStore, MoneySubTab } from '../../store/uiStore';
import { ExecutiveDashboardView } from '../analytics/ExecutiveDashboardView';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';

export const MoneyHubView: React.FC = () => {
  const { moneySubTab, setMoneySubTab } = useUIStore();

  const subTabs: { id: MoneySubTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'invoices', label: 'Invoices & Receivables', icon: <DollarSign size={15} />, badge: '€182k Total' },
    { id: 'realization', label: 'Bank Realization & eBRC', icon: <CheckCircle2 size={15} />, badge: '2 Pending' },
    { id: 'margins', label: 'Realized Margins & RoDTEP', icon: <TrendingUp size={15} /> },
    { id: 'analytics', label: 'Executive Revenue KPIs', icon: <BarChart3 size={15} /> },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header with Sub-Navigation */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-5 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Money & Finance Hub</h2>
              <AppleBadge tone="green" size="sm">Export Treasury</AppleBadge>
              <TruthStatusBadge status="verified" sourceName="Bank EDPMS & DGFT Portal" checkedDate="30 Aug 2026" />
            </div>
            <p className="text-xs text-slate-500 font-medium mt-1">
              Track foreign exchange receipts, monitor bank eBRC settlements, reconcile RoDTEP incentives, and analyze export profitability.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <WhatDoesThisMean term="eBRC (Electronic Bank Realization Certificate)" label="eBRC Guide" />
            <WhatDoesThisMean term="Duty Drawback & RoDTEP" label="Incentives Guide" />
          </div>
        </div>

        {/* Apple HIG Sub-Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto p-1 bg-slate-100/80 rounded-2xl border border-slate-200/60">
          {subTabs.map((tab) => {
            const isActive = moneySubTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setMoneySubTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                  isActive
                    ? 'bg-white text-slate-900 shadow-xs border border-slate-200/80 scale-[1.01]'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                }`}
              >
                <span className={isActive ? 'text-emerald-600' : 'text-slate-400'}>{tab.icon}</span>
                <span>{tab.label}</span>
                {tab.badge && (
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-md font-mono ${
                    isActive ? 'bg-emerald-100 text-emerald-800 font-bold' : 'bg-slate-200 text-slate-600 font-medium'
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
      {moneySubTab === 'invoices' && <InvoicesAndReceivablesPanel />}
      {moneySubTab === 'realization' && <BankRealizationAndEbrcPanel />}
      {moneySubTab === 'margins' && <MarginsAndIncentivesPanel />}
      {moneySubTab === 'analytics' && <ExecutiveDashboardView />}
    </div>
  );
};

const InvoicesAndReceivablesPanel: React.FC = () => {
  const invoices = [
    {
      invNo: 'EXP-INV-2026-042',
      buyer: 'Bader GmbH & Co. KG',
      date: '14 Aug 2026',
      dueDate: '13 Sep 2026',
      terms: '30 Days Net from B/L Date',
      amountEur: 85500,
      amountInr: '₹78.23 Lakh',
      status: 'Awaiting Remittance',
      statusTone: 'orange' as const,
      truth: 'declared'
    },
    {
      invNo: 'EXP-INV-2026-039',
      buyer: 'Picard Lederwaren GmbH',
      date: '28 Jul 2026',
      dueDate: '27 Aug 2026',
      terms: 'LC at Sight (Irrevocable Confirmed)',
      amountEur: 37200,
      amountInr: '₹34.03 Lakh',
      status: 'Realized in Bank (eBRC Generated)',
      statusTone: 'green' as const,
      truth: 'verified'
    },
    {
      invNo: 'EXP-INV-2026-031',
      buyer: 'Roeckl Handschuhe',
      date: '10 Jul 2026',
      dueDate: '09 Aug 2026',
      terms: 'Advance 30% / Balance 70% against Docs',
      amountEur: 17000,
      amountInr: '₹15.55 Lakh',
      status: 'Realized in Bank (eBRC Generated)',
      statusTone: 'green' as const,
      truth: 'verified'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <AppleCard variant="default" className="bg-white border-slate-200 p-4">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Total Outstanding Invoices</span>
          <p className="text-2xl font-extrabold font-mono text-slate-900 mt-1">€85,500 <span className="text-xs font-normal text-slate-500 font-sans">(₹78.23 Lakh)</span></p>
          <p className="text-xs text-amber-700 font-medium mt-1">1 active invoice due in 14 days</p>
        </AppleCard>
        <AppleCard variant="default" className="bg-white border-slate-200 p-4">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Realized YTD Revenue</span>
          <p className="text-2xl font-extrabold font-mono text-emerald-700 mt-1">€54,200 <span className="text-xs font-normal text-slate-500 font-sans">(₹49.58 Lakh)</span></p>
          <p className="text-xs text-slate-500 font-medium mt-1">100% FX realized to Indian Bank Account</p>
        </AppleCard>
        <AppleCard variant="default" className="bg-white border-slate-200 p-4">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Average DSO (Days Sales Out)</span>
          <p className="text-2xl font-extrabold font-mono text-blue-700 mt-1">26 Days</p>
          <p className="text-xs text-slate-500 font-medium mt-1">4 days faster than industry average</p>
        </AppleCard>
      </div>

      <div className="bg-white border border-slate-200/90 rounded-2xl overflow-hidden shadow-xs">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900">Commercial Invoices Registry</h3>
          <AppleButton variant="secondary" size="sm">Export to Tally / Excel</AppleButton>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 font-bold border-b border-slate-200/60 uppercase tracking-wider text-[10px]">
              <tr>
                <th className="p-3.5">Invoice No</th>
                <th className="p-3.5">Buyer</th>
                <th className="p-3.5">Issue Date</th>
                <th className="p-3.5">Due Date</th>
                <th className="p-3.5">Payment Terms</th>
                <th className="p-3.5 text-right">Amount (EUR / INR)</th>
                <th className="p-3.5">Status</th>
                <th className="p-3.5">Truth Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {invoices.map((inv) => (
                <tr key={inv.invNo} className="hover:bg-slate-50/80 transition-colors font-medium">
                  <td className="p-3.5 font-mono font-bold text-blue-600">{inv.invNo}</td>
                  <td className="p-3.5 font-bold text-slate-900">{inv.buyer}</td>
                  <td className="p-3.5 text-slate-500">{inv.date}</td>
                  <td className="p-3.5 text-slate-500">{inv.dueDate}</td>
                  <td className="p-3.5 text-slate-600 text-[11px]">{inv.terms}</td>
                  <td className="p-3.5 text-right font-mono">
                    <span className="font-bold text-slate-900">€{inv.amountEur.toLocaleString()}</span>
                    <span className="block text-[10px] text-slate-500">{inv.amountInr}</span>
                  </td>
                  <td className="p-3.5">
                    <AppleBadge tone={inv.statusTone} size="sm">{inv.status}</AppleBadge>
                  </td>
                  <td className="p-3.5">
                    <TruthStatusBadge status={inv.truth} sourceName="Invoice Vault" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const BankRealizationAndEbrcPanel: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="bg-emerald-50/70 border border-emerald-200/80 rounded-2xl p-4 flex items-start gap-3">
        <FileCheck className="w-5 h-5 text-emerald-700 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h4 className="text-xs font-bold text-emerald-950">DGFT eBRC Realization Gateway</h4>
          <p className="text-xs text-emerald-800 leading-relaxed font-medium">
            Trade OS connects your Indian Authorized Dealer (AD) bank Inward Remittance Messages (IRM) directly with Indian Customs Shipping Bills to automatically monitor EDPMS closure.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AppleCard variant="default" className="bg-white border-slate-200 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-slate-900">eBRC Realization Status (Picard Order)</h4>
            <TruthStatusBadge status="verified" sourceName="State Bank of India (AD Code: 0210041)" checkedDate="18 Aug 2026" />
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl space-y-2 text-xs font-medium">
            <div className="flex justify-between">
              <span className="text-slate-500">Shipping Bill No:</span>
              <span className="font-mono font-bold text-slate-800">SB-8921044 / Chennai Port</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">FOB Value Declared:</span>
              <span className="font-mono font-bold text-slate-800">€37,200 (₹34,03,800)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Foreign Exchange Received:</span>
              <span className="font-mono font-bold text-emerald-700">€37,200 via SWIFT wire</span>
            </div>
            <div className="flex justify-between border-t border-slate-200 pt-1.5">
              <span className="text-slate-500">eBRC Certificate ID:</span>
              <span className="font-mono font-bold text-blue-700">eBRC-SBI-2026-884102</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">EDPMS Realization Status:</span>
              <span className="font-bold text-emerald-700">CLOSED (100% Realized)</span>
            </div>
          </div>
        </AppleCard>

        <AppleCard variant="default" className="bg-white border-slate-200 p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-slate-900">Pending Realization (Bader Order)</h4>
            <TruthStatusBadge status="declared" sourceName="HDFC Bank AD" checkedDate="29 Aug 2026" />
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl space-y-2 text-xs font-medium">
            <div className="flex justify-between">
              <span className="text-slate-500">Shipping Bill No:</span>
              <span className="font-mono font-bold text-slate-800">SB-9102431 / Chennai Port</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">FOB Value Declared:</span>
              <span className="font-mono font-bold text-slate-800">€85,500 (₹78,23,250)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Payment Due:</span>
              <span className="font-mono font-bold text-amber-700">13 Sep 2026 (14 Days Remaining)</span>
            </div>
            <div className="flex justify-between border-t border-slate-200 pt-1.5">
              <span className="text-slate-500">eBRC Filing Status:</span>
              <span className="font-bold text-slate-600">Pending Inward Remittance IRM</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">EDPMS Realization Status:</span>
              <span className="font-bold text-amber-600">OPEN / UNREALIZED</span>
            </div>
          </div>
        </AppleCard>
      </div>
    </div>
  );
};

const MarginsAndIncentivesPanel: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AppleCard variant="default" className="bg-white border-slate-200 p-5 space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-slate-900">RoDTEP & Duty Drawback Receivable</h4>
            <TruthStatusBadge status="verified" sourceName="DGFT Schedule 2026" />
          </div>
          <p className="text-xs text-slate-500">Government export incentives calculated on finished leather exports under Chapter 41.</p>
          
          <div className="p-3.5 bg-slate-50 rounded-xl space-y-2 text-xs font-medium">
            <div className="flex justify-between">
              <span className="text-slate-600">RoDTEP Rate (HS 4107):</span>
              <span className="font-mono font-bold text-slate-800">1.8% of FOB Value</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-600">All Industry Duty Drawback:</span>
              <span className="font-mono font-bold text-slate-800">2.1% of FOB Value</span>
            </div>
            <div className="flex justify-between border-t border-slate-200 pt-1.5">
              <span className="text-slate-600">Combined Incentive Receivable:</span>
              <span className="font-mono font-bold text-emerald-700">3.9% (₹4.38 Lakh YTD)</span>
            </div>
          </div>
        </AppleCard>

        <AppleCard variant="default" className="bg-white border-slate-200 p-5 space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-slate-900">Landed Cost & Net Realized Margin</h4>
            <TruthStatusBadge status="estimated" sourceName="Trade OS Margin Engine" />
          </div>
          <p className="text-xs text-slate-500">Live reconciliation of manufacturing cost, sea freight, customs duty, and foreign exchange conversion.</p>
          
          <div className="p-3.5 bg-slate-50 rounded-xl space-y-2 text-xs font-medium">
            <div className="flex justify-between">
              <span className="text-slate-600">Average Production Cost:</span>
              <span className="font-mono font-bold text-slate-800">₹182 / sqft</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-600">Average FOB Realization:</span>
              <span className="font-mono font-bold text-slate-800">€2.95 (₹269.90 / sqft)</span>
            </div>
            <div className="flex justify-between border-t border-slate-200 pt-1.5">
              <span className="text-slate-600">Net Realized Gross Margin:</span>
              <span className="font-mono font-extrabold text-emerald-700">28.4% (Including RoDTEP)</span>
            </div>
          </div>
        </AppleCard>
      </div>
    </div>
  );
};
