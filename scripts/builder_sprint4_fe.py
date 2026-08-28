import os

def w(path, content):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"[CREATED] {path}")

# 1. frontend/src/api/customs.ts
w("frontend/src/api/customs.ts", """import { fetchApi } from './client';

export interface CustomsShipmentItem {
  id: string;
  bol_number: string;
  shipment_date: string;
  importer_name: string;
  exporter_name: string;
  origin_port: string;
  destination_port: string;
  hs_code: string;
  product_desc: string;
  weight_kg: number;
  teu_count: number;
  declared_value_usd?: number;
}

export interface CustomsShipmentsListResponse {
  total_count: number;
  shipments: CustomsShipmentItem[];
}

export const getCustomsShipmentsApi = (limit: number = 50) =>
  fetchApi<CustomsShipmentsListResponse>(`/api/v1/customs/shipments?limit=${limit}`);
""")

# 2. frontend/src/api/crm.ts
w("frontend/src/api/crm.ts", """import { fetchApi } from './client';

export interface CRMExportResponse {
  export_id: string;
  buyer_id: string;
  buyer_name: string;
  format: string;
  status: string;
  payload: Record<string, any>;
  download_url?: string;
  message: string;
}

export const exportCRM = (buyerId: string, format: 'hubspot' | 'salesforce' | 'csv') =>
  fetchApi<CRMExportResponse>('/api/v1/crm/export', {
    method: 'POST',
    body: JSON.stringify({ buyer_id: buyerId, export_format: format }),
  });
""")

# 3. frontend/src/components/customs/CustomsExplorerView.tsx
w("frontend/src/components/customs/CustomsExplorerView.tsx", """import React, { useEffect, useState } from 'react';
import { Anchor, Ship, FileText, ArrowRight, TrendingUp, DollarSign, Box } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { PageSkeleton } from '../ui/PageSkeleton';
import { getCustomsShipmentsApi, CustomsShipmentItem } from '../../api/customs';

export const CustomsExplorerView: React.FC = () => {
  const [shipments, setShipments] = useState<CustomsShipmentItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getCustomsShipmentsApi(50)
      .then(res => setShipments(res.shipments))
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <PageSkeleton />;

  const totalTEU = shipments.reduce((acc, s) => acc + s.teu_count, 0);
  const totalValue = shipments.reduce((acc, s) => acc + (s.declared_value_usd || 0), 0);

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Banner */}
      <div className="p-6 rounded-3xl bg-gradient-to-r from-blue-950/40 via-zinc-900/80 to-zinc-900/40 border border-blue-500/20 backdrop-blur-2xl">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-1.5 rounded-lg bg-blue-500/20 text-blue-400">
                <Ship size={18} />
              </span>
              <h2 className="text-xl font-bold text-white tracking-tight">Customs Bill of Lading (BOL) Manifest Flows</h2>
            </div>
            <p className="text-xs text-zinc-400 max-w-2xl">
              Real-time ocean manifest records connecting Indian export hubs (Chennai, Tuticorin, Kolkata) to European discharge ports (Hamburg, Genoa, Le Havre).
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2 bg-zinc-900/80 border border-white/[0.08] rounded-xl text-center">
              <div className="text-[10px] uppercase font-semibold text-zinc-500">Tracked Containers</div>
              <div className="text-base font-bold text-white font-mono">{totalTEU} FEU</div>
            </div>
            <div className="px-4 py-2 bg-zinc-900/80 border border-white/[0.08] rounded-xl text-center">
              <div className="text-[10px] uppercase font-semibold text-zinc-500">Verified Manifest Value</div>
              <div className="text-base font-bold text-emerald-400 font-mono">${(totalValue / 1000).toFixed(0)}k USD</div>
            </div>
          </div>
        </div>
      </div>

      {/* Shipment Manifest Stream */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs font-semibold text-zinc-400 uppercase tracking-wider px-1">
          <span>Recent Ocean Manifests ({shipments.length})</span>
          <span>Verified Port Customs Clearance</span>
        </div>

        {shipments.map((s) => (
          <AppleCard key={s.id} variant="default" className="p-4 hover:border-blue-500/40 transition-all">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono text-xs font-bold text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                    {s.bol_number}
                  </span>
                  <h4 className="text-sm font-bold text-white">{s.importer_name}</h4>
                  <AppleBadge tone="blue" size="sm">HS {s.hs_code}</AppleBadge>
                </div>
                <p className="text-xs text-zinc-300">{s.product_desc}</p>
                <div className="flex items-center gap-4 text-[11px] text-zinc-500">
                  <span>Shipper: <b className="text-zinc-400">{s.exporter_name}</b></span>
                  <span>Weight: <b className="text-zinc-400">{s.weight_kg.toLocaleString()} kg</b></span>
                  <span>Date: <b className="text-zinc-400">{s.shipment_date}</b></span>
                </div>
              </div>

              <div className="flex items-center gap-4 border-t md:border-t-0 md:border-l border-white/[0.08] pt-3 md:pt-0 md:pl-6">
                <div className="flex items-center gap-2 text-xs font-mono">
                  <span className="px-2 py-1 bg-zinc-800 text-zinc-300 rounded">{s.origin_port}</span>
                  <ArrowRight size={13} className="text-zinc-500" />
                  <span className="px-2 py-1 bg-zinc-800 text-zinc-300 rounded">{s.destination_port}</span>
                </div>
                {s.declared_value_usd && (
                  <div className="text-right font-mono text-xs text-emerald-400 font-bold">
                    ${s.declared_value_usd.toLocaleString()}
                  </div>
                )}
              </div>
            </div>
          </AppleCard>
        ))}
      </div>
    </div>
  );
};
""")

# 4. frontend/src/components/accounts/CRMExportModal.tsx
w("frontend/src/components/accounts/CRMExportModal.tsx", """import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, FileText, CheckCircle2, Share2, Copy } from 'lucide-react';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { exportCRM, CRMExportResponse } from '../../api/crm';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  buyerId: string;
  buyerName: string;
}

export const CRMExportModal: React.FC<Props> = ({ isOpen, onClose, buyerId, buyerName }) => {
  const [selectedFormat, setSelectedFormat] = useState<'hubspot' | 'salesforce' | 'csv'>('hubspot');
  const [isExporting, setIsExporting] = useState(false);
  const [exportResult, setExportResult] = useState<CRMExportResponse | null>(null);

  const handleExport = async () => {
    setIsExporting(true);
    try {
      const res = await exportCRM(buyerId, selectedFormat);
      setExportResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/70 backdrop-blur-md"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="relative w-full max-w-lg bg-zinc-900/95 border border-white/[0.12] rounded-3xl shadow-2xl backdrop-blur-3xl p-6 space-y-5 z-10"
          >
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <h3 className="text-lg font-bold text-white">Enterprise CRM Export</h3>
                <p className="text-xs text-zinc-400">Export dossier & outreach pack for {buyerName}</p>
              </div>
              <AppleBadge tone="blue" size="sm">Enterprise $2,500/mo</AppleBadge>
            </div>

            <div className="grid grid-cols-3 gap-2">
              {(['hubspot', 'salesforce', 'csv'] as const).map((fmt) => (
                <button
                  key={fmt}
                  onClick={() => {
                    setSelectedFormat(fmt);
                    setExportResult(null);
                  }}
                  className={`p-3 rounded-2xl border text-center transition-all ${
                    selectedFormat === fmt
                      ? 'bg-blue-500/10 border-blue-500/40 text-blue-300 font-bold'
                      : 'bg-zinc-950/40 border-white/[0.06] text-zinc-400 hover:text-white'
                  }`}
                >
                  <div className="text-xs uppercase">{fmt}</div>
                </button>
              ))}
            </div>

            {exportResult ? (
              <div className="space-y-3">
                <div className="p-3.5 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl text-xs text-emerald-300 flex items-center gap-2">
                  <CheckCircle2 size={16} />
                  <span>{exportResult.message}</span>
                </div>

                <div className="p-3 bg-zinc-950 rounded-2xl border border-white/[0.06] max-h-48 overflow-y-auto">
                  <pre className="text-[10px] font-mono text-zinc-300 whitespace-pre-wrap">
                    {JSON.stringify(exportResult.payload, null, 2)}
                  </pre>
                </div>
              </div>
            ) : (
              <p className="text-xs text-zinc-400">
                Exports verified contact details, match score breakdown, EUDR article readiness declaration, and generated outreach draft.
              </p>
            )}

            <div className="flex items-center justify-end gap-3 pt-2">
              <AppleButton variant="ghost" size="sm" onClick={onClose}>Close</AppleButton>
              <AppleButton
                variant="primary"
                size="sm"
                loading={isExporting}
                onClick={handleExport}
                icon={<Download size={14} />}
              >
                {exportResult ? 'Re-Export' : 'Generate Export'}
              </AppleButton>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
};
""")
