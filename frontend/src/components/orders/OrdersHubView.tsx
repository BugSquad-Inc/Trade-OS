import React from 'react';
import { Layers, FileCheck, Ship, Anchor, ArrowRight } from 'lucide-react';
import { useUIStore, OrdersSubTab } from '../../store/uiStore';
import { DealsPipelineView } from '../deals/DealsPipelineView';
import { DocumentPackView } from '../documents/DocumentPackView';
import { ShipmentMilestoneTrackerView } from '../shipments/ShipmentMilestoneTrackerView';
import { CustomsExplorerView } from '../customs/CustomsExplorerView';
import { AppleBadge } from '../apple/AppleBadge';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';

export const OrdersHubView: React.FC = () => {
  const { ordersSubTab, setOrdersSubTab } = useUIStore();

  const subTabs: { id: OrdersSubTab; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: 'deals', label: '12-Stage Export Pipeline', icon: <Layers size={15} />, badge: '3 Deals' },
    { id: 'documents', label: 'Export Document Vault', icon: <FileCheck size={15} />, badge: 'EUDR Ready' },
    { id: 'shipments', label: 'Ocean Shipments & Radar', icon: <Ship size={15} />, badge: 'Live Track' },
    { id: 'customs', label: 'Port Customs Displacements', icon: <Anchor size={15} /> },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header with Sub-Navigation */}
      <div className="bg-white border border-slate-200/90 rounded-3xl p-5 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Orders & Fulfilment Hub</h2>
              <AppleBadge tone="blue" size="sm">Stage-Gated Operations</AppleBadge>
              <TruthStatusBadge status="verified" sourceName="DGFT Shipping Bills" checkedDate="30 Aug 2026" />
            </div>
            <p className="text-xs text-slate-500 font-medium mt-1">
              Track export manufacturing progress, assemble customs & EUDR document packs, and track container voyages to European ports.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <WhatDoesThisMean term="EUDR (EU Deforestation Regulation)" label="Document Checklist Help" />
          </div>
        </div>

        {/* Apple HIG Sub-Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto p-1 bg-slate-100/80 rounded-2xl border border-slate-200/60">
          {subTabs.map((tab) => {
            const isActive = ordersSubTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setOrdersSubTab(tab.id)}
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
      {ordersSubTab === 'deals' && <DealsPipelineView />}
      {ordersSubTab === 'documents' && <DocumentPackView />}
      {ordersSubTab === 'shipments' && <ShipmentMilestoneTrackerView />}
      {ordersSubTab === 'customs' && <CustomsExplorerView />}
    </div>
  );
};
