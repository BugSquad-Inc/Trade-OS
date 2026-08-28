import React, { useState } from 'react';
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
              <AppleButton variant="secondary" size="sm" onClick={onClose}>Close</AppleButton>
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
