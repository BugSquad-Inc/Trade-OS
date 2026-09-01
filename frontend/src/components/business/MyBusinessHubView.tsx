import React from 'react';
import { Building2, Layers, CheckCircle, Users, ShieldCheck, CheckCircle2, Award, FileText } from 'lucide-react';
import { useUIStore, BusinessSubTab } from '../../store/uiStore';
import { ProductPassportView } from '../products/ProductPassportView';
import { VerificationQueueView } from '../verification/VerificationQueueView';
import { AuditTrailView } from '../audit/AuditTrailView';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';

export const MyBusinessHubView: React.FC = () => {
  const { businessSubTab, setBusinessSubTab, setOnboardingModalOpen, setTeamModalOpen } = useUIStore();

  const subTabs: { id: BusinessSubTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'profile', label: 'Exporter Profile & Readiness', icon: <Building2 size={15} />, badge: '95/100' },
    { id: 'products', label: 'Digital Product Passports', icon: <Layers size={15} />, badge: '20 Specs' },
    { id: 'verification', label: 'Buyer Verification Queue', icon: <CheckCircle size={15} />, badge: '5 Pending' },
    { id: 'team', label: 'Team Roles & Permissions', icon: <Users size={15} />, badge: '13 Users' },
    { id: 'audit', label: 'Compliance Audit Trail', icon: <ShieldCheck size={15} /> },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header with Sub-Navigation */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-5 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">My Business Hub</h2>
              <AppleBadge tone="purple" size="sm">Organization Administration</AppleBadge>
              <TruthStatusBadge status="verified" sourceName="DGFT Verified IEC & GSTIN" checkedDate="30 Aug 2026" />
            </div>
            <p className="text-xs text-slate-500 font-medium mt-1">
              Manage Butler's Leather factory capability, configure product specifications and lab test certificates, and oversee team access.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <WhatDoesThisMean term="LWG (Leather Working Group)" label="LWG Audit Help" />
            <WhatDoesThisMean term="Digital Product Passport (DPP)" label="DPP Help" />
          </div>
        </div>

        {/* Apple HIG Sub-Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto p-1 bg-slate-100/80 rounded-2xl border border-slate-200/60">
          {subTabs.map((tab) => {
            const isActive = businessSubTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setBusinessSubTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
                  isActive
                    ? 'bg-white text-slate-900 shadow-xs border border-slate-200/80 scale-[1.01]'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                }`}
              >
                <span className={isActive ? 'text-purple-600' : 'text-slate-400'}>{tab.icon}</span>
                <span>{tab.label}</span>
                {tab.badge && (
                  <span className={`text-[10px] px-1.5 py-0.2 rounded-md font-mono ${
                    isActive ? 'bg-purple-100 text-purple-700 font-bold' : 'bg-slate-200 text-slate-600 font-medium'
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
      {businessSubTab === 'profile' && <ExporterProfileSummaryPanel />}
      {businessSubTab === 'products' && <ProductPassportView />}
      {businessSubTab === 'verification' && <VerificationQueueView />}
      {businessSubTab === 'team' && <TeamManagementEmbeddedPanel />}
      {businessSubTab === 'audit' && <AuditTrailView />}
    </div>
  );
};

const ExporterProfileSummaryPanel: React.FC = () => {
  const { setOnboardingModalOpen } = useUIStore();

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Factory Profile Overview */}
        <AppleCard variant="default" className="md:col-span-2 bg-white border-slate-200 p-6 space-y-4">
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-900">Butler's Leather Tannery Pvt Ltd</h3>
                <TruthStatusBadge status="verified" sourceName="DGFT & MCA Portal" />
              </div>
              <p className="text-xs text-slate-500 font-medium">Ambur Leather Cluster · Tamil Nadu, India · Established 1988</p>
            </div>

            <AppleButton variant="secondary" size="sm" onClick={() => setOnboardingModalOpen(true)}>
              Edit Full Profile
            </AppleButton>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">IEC Code</span>
              <span className="font-mono font-bold text-slate-900">0408012941</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">GSTIN</span>
              <span className="font-mono font-bold text-slate-900">33AABCB1234F1Z5</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">RCMC / CLE</span>
              <span className="font-mono font-bold text-slate-900">CLE/SR/RCMC/2024</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Monthly Capacity</span>
              <span className="font-bold text-slate-900">50,000 sqft / month</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Standard MOQ</span>
              <span className="font-bold text-slate-900">3,000 sqft per article</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs">
              <span className="text-slate-400 block text-[10px] uppercase font-bold">Sample Turnaround</span>
              <span className="font-bold text-emerald-700">7 Days by Air</span>
            </div>
          </div>
        </AppleCard>

        {/* Export Readiness & Compliance Score */}
        <AppleCard variant="default" className="bg-white border-slate-200 p-6 space-y-4 flex flex-col justify-between">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Export Readiness</span>
              <AppleBadge tone="green" size="sm">EU Export Ready</AppleBadge>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-extrabold font-mono text-emerald-700">95</span>
              <span className="text-sm font-bold text-slate-400">/ 100</span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed font-medium">
              Butler's Leather meets all mandatory chemical, traceability, and documentation thresholds for European market entry.
            </p>
          </div>

          <div className="space-y-1.5 pt-2 border-t border-slate-100 text-xs">
            <div className="flex items-center justify-between text-slate-700 font-medium">
              <span className="flex items-center gap-1.5"><Award size={13} className="text-amber-500" /> LWG Environmental Audit:</span>
              <span className="font-bold text-emerald-700">Gold Rated</span>
            </div>
            <div className="flex items-center justify-between text-slate-700 font-medium">
              <span className="flex items-center gap-1.5"><ShieldCheck size={13} className="text-blue-500" /> REACH Lab Test Compliance:</span>
              <span className="font-bold text-emerald-700">Passed (TUV)</span>
            </div>
            <div className="flex items-center justify-between text-slate-700 font-medium">
              <span className="flex items-center gap-1.5"><FileText size={13} className="text-teal-500" /> EUDR Abattoir Geolocation:</span>
              <span className="font-bold text-emerald-700">Mapped</span>
            </div>
          </div>
        </AppleCard>
      </div>
    </div>
  );
};

const TeamManagementEmbeddedPanel: React.FC = () => {
  const { setTeamModalOpen } = useUIStore();

  const members = [
    { name: 'Johann Butler', role: 'Owner & Managing Director', email: 'johann@butlers.in', access: 'Full Admin & Sign-Off' },
    { name: 'Ramesh Sundaram', role: 'Head of Export Sales', email: 'ramesh.sales@butlers.in', access: 'Sales, Outreach & Quotes' },
    { name: 'Ananya Krishnan', role: 'Compliance & Quality Lead', email: 'ananya.compliance@butlers.in', access: 'Lab Reports & EUDR' },
    { name: 'Vikram Mehta', role: 'Finance & Accounts Manager', email: 'vikram.finance@butlers.in', access: 'Invoices, eBRC & Margins' }
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">Role-Based Team Members (RBAC)</h3>
          <p className="text-xs text-slate-500 font-medium">Granular permissions protecting compliance approvals and commercial quotations.</p>
        </div>
        <AppleButton variant="primary" size="sm" onClick={() => setTeamModalOpen(true)}>
          Invite Team Member
        </AppleButton>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {members.map((m) => (
          <AppleCard key={m.email} variant="default" className="bg-white border-slate-200 p-4 space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-bold text-slate-900">{m.name}</h4>
              <AppleBadge tone="blue" size="sm">{m.role}</AppleBadge>
            </div>
            <p className="text-xs text-slate-500 font-mono">{m.email}</p>
            <p className="text-[11px] text-slate-600 pt-1 border-t border-slate-100 font-medium">
              <b>Permissions:</b> {m.access}
            </p>
          </AppleCard>
        ))}
      </div>
    </div>
  );
};
