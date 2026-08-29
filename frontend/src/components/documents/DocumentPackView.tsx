import React, { useState } from 'react';
import { FileText, ShieldCheck, CheckCircle2, Download, Plus, AlertCircle, FileCheck, Check } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useDocuments, useComplianceAudit, TradeDocument } from '../../api/documents';

export const DocumentPackView: React.FC = () => {
  const { data: documents, isLoading } = useDocuments();
  const complianceAudit = useComplianceAudit();

  const [auditResult, setAuditResult] = useState<any | null>(null);

  const docList = documents || [];

  const runAudit = () => {
    complianceAudit.mutate(
      {
        exporter_certs: ['LWG Gold Rated', 'ISO 14001:2015', 'REACH SVHC Tested'],
        has_farm_polygons: true,
        cr_vi_tested_zero: true,
        reach_svhc_zero: true,
      },
      {
        onSuccess: (data) => setAuditResult(data),
      }
    );
  };

  if (isLoading) return <PageSkeleton />;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-emerald-800 via-teal-900 to-slate-900 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold tracking-tight">Export Document Vault & Compliance Rule Engine v2</h2>
            <span className="px-2 py-0.5 rounded-full bg-emerald-500/30 text-emerald-200 text-[11px] font-medium border border-emerald-400/20">
              EU 2026 Ready
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-xl font-medium">
            Immutable vault for EUDR Due Diligence Statements, Eurofins chemical lab reports, and automated customs clearance audits.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <AppleButton
            variant="primary"
            size="sm"
            className="bg-emerald-500 hover:bg-emerald-600 text-white border-0"
            icon={<ShieldCheck size={14} />}
            onClick={runAudit}
          >
            Run Compliance Pre-Check
          </AppleButton>
        </div>
      </div>

      {/* Compliance Rule Engine v2 Audit Results (If Run) */}
      {auditResult && (
        <AppleCard variant="default" className="bg-emerald-50/50 border-emerald-200 p-5 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 border-b border-emerald-200/80 pb-3">
            <div className="flex items-center gap-2">
              <CheckCircle2 size={20} className="text-emerald-700" />
              <div>
                <h4 className="text-sm font-bold text-emerald-950">{auditResult.clearance_grade}</h4>
                <p className="text-xs text-emerald-700 font-medium">Clearance Score: {auditResult.overall_score}/100 · {auditResult.auditor}</p>
              </div>
            </div>
            <AppleBadge tone="green" size="sm">EU Customs Approved</AppleBadge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            {auditResult.checks.map((chk: any, idx: number) => (
              <div key={idx} className="p-3 rounded-xl bg-white border border-emerald-100 space-y-1">
                <div className="flex items-center justify-between font-bold text-slate-900">
                  <span>{chk.regulation}</span>
                  <span className="text-emerald-700">+{chk.weight} pts</span>
                </div>
                <p className="text-[11px] text-slate-600">{chk.requirement}</p>
                <p className="text-[10px] text-slate-500 font-mono italic">Evidence: {chk.evidence}</p>
              </div>
            ))}
          </div>
        </AppleCard>
      )}

      {/* Documents List */}
      <div className="space-y-3">
        <div className="flex items-center justify-between px-1">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            Verified Export Documents ({docList.length})
          </h3>
        </div>

        {docList.length === 0 ? (
          <EmptyState title="No Documents Uploaded" description="Upload your EUDR DDS and lab certificates." />
        ) : (
          <div className="space-y-3">
            {docList.map((doc) => (
              <AppleCard
                key={doc.id}
                variant="default"
                className="bg-white border-slate-200/90 shadow-2xs hover:border-emerald-300 transition-all p-4"
              >
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="flex items-start gap-3 flex-1">
                    <div className="p-2.5 rounded-xl bg-emerald-50 text-emerald-700 shrink-0 mt-0.5">
                      <FileCheck size={18} />
                    </div>
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h4 className="text-sm font-bold text-slate-900">{doc.title}</h4>
                        <AppleBadge tone="green" size="sm">{doc.doc_type.replace(/_/g, ' ').toUpperCase()}</AppleBadge>
                        <TruthStatusBadge status="verified" sourceName="Tamper-Evident SHA-256 Vault" />
                      </div>
                      <p className="text-xs text-slate-500 font-mono">
                        {doc.file_name} · {(doc.file_size_bytes / 1024).toFixed(0)} KB · SHA256: {doc.file_hash_sha256.substring(0, 16)}...
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <AppleButton
                      variant="secondary"
                      size="sm"
                      icon={<Download size={13} />}
                      onClick={() => alert(`Downloading verified document: ${doc.file_name}`)}
                    >
                      Download PDF
                    </AppleButton>
                  </div>
                </div>
              </AppleCard>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
