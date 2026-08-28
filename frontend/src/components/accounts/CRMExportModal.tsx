import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, CheckCircle2 } from 'lucide-react';
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
            className="fixed inset-0 bg-slate-900/30 backdrop-blur-md"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="relative w-full max-w-lg bg-white/95 border border-slate-200/90 rounded-3xl shadow-2xl backdrop-blur-3xl p-6 space-y-5 z-10 text-slate-900"
          >
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <h3 className="text-lg font-bold text-slate-900">Enterprise CRM Export</h3>
                <p className="text-xs text-slate-500 font-medium">Export dossier & outreach pack for {buyerName}</p>
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
                  className={`p-3 rounded-2xl border text-center transition-all cursor-pointer ${
                    selectedFormat === fmt
                      ? 'bg-blue-50 border-blue-300 text-blue-700 font-bold shadow-2xs'
                      : 'bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <div className="text-xs uppercase">{fmt}</div>
                </button>
              ))}
            </div>

            {exportResult ? (
              <div className="space-y-3">
                <div className="p-3.5 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-800 font-medium flex items-center gap-2">
                  <CheckCircle2 size={16} className="text-emerald-600" />
                  <span>{exportResult.message}</span>
                </div>

                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200 max-h-48 overflow-y-auto shadow-inner">
                  <pre className="text-[10px] font-mono text-slate-700 whitespace-pre-wrap">
                    {JSON.stringify(exportResult.payload, null, 2)}
                  </pre>
                </div>
              </div>
            ) : (
              <p className="text-xs text-slate-500 leading-relaxed">
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
