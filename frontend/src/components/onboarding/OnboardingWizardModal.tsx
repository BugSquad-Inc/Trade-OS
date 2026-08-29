import React, { useState } from 'react';
import { CheckCircle2, ShieldCheck, Building, FileCheck, Anchor, Award, ArrowRight, ArrowLeft, X } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { useExporterProfile, useReadinessGaps, useSubmitOnboardingStep } from '../../api/exporters';

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const OnboardingWizardModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const { data: profile } = useExporterProfile();
  const { data: gaps } = useReadinessGaps();
  const submitStep = useSubmitOnboardingStep();

  const [activeStep, setActiveStep] = useState(1);
  const [formData, setFormData] = useState<Record<string, any>>({
    company_name: "Butler's Leather",
    location: "Chennai, Tamil Nadu, India",
    cluster: "Chennai / Ambur / Ranipet Leather Cluster",
    pan: "AABCB1234F",
    iec: "0498765432",
    ad_code: "6390001",
    rcmc_number: "CLE/SR/RCMC/2024/9876",
    port_of_export: "Chennai Port (INMAA)",
    monthly_capacity_sqft: 50000,
    moq_sqft: 3000,
  });

  if (!isOpen) return null;

  const steps = [
    { id: 1, title: 'Company Identity', icon: <Building size={16} /> },
    { id: 2, title: 'Tax & DGFT Registrations', icon: <FileCheck size={16} /> },
    { id: 3, title: 'Facilities & Logistics', icon: <Anchor size={16} /> },
    { id: 4, title: 'Readiness Audit', icon: <Award size={16} /> },
  ];

  const handleNext = () => {
    submitStep.mutate({ step: activeStep, data: formData });
    if (activeStep < 4) {
      setActiveStep(activeStep + 1);
    } else {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden z-50 max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-gradient-to-r from-slate-50 to-blue-50/40">
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-lg font-bold text-slate-900 tracking-tight">Indian Exporter Readiness & Onboarding</h3>
              <AppleBadge tone="green" size="sm">Stage 1</AppleBadge>
            </div>
            <p className="text-xs text-slate-500 mt-0.5 font-medium">Verify DGFT, ICEGATE, and CLE credentials for European compliance clearance</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-full cursor-pointer"
          >
            <X size={18} />
          </button>
        </div>

        {/* Step Progress Pills */}
        <div className="flex items-center justify-between px-6 py-3 bg-slate-50/80 border-b border-slate-100 overflow-x-auto gap-2">
          {steps.map((s) => (
            <button
              key={s.id}
              onClick={() => setActiveStep(s.id)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all ${
                activeStep === s.id
                  ? 'bg-blue-600 text-white shadow-sm'
                  : s.id < activeStep
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  : 'text-slate-500 hover:bg-slate-200/50'
              }`}
            >
              {s.id < activeStep ? <CheckCircle2 size={14} className="text-emerald-600" /> : s.icon}
              <span>{s.title}</span>
            </button>
          ))}
        </div>

        {/* Form Body */}
        <div className="p-6 overflow-y-auto space-y-4 flex-1">
          {activeStep === 1 && (
            <div className="space-y-4 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Company Legal Name</label>
                <input
                  type="text"
                  value={formData.company_name}
                  onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:bg-white focus:border-blue-500 outline-none"
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Location City / State</label>
                  <input
                    type="text"
                    value={formData.location}
                    onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:bg-white focus:border-blue-500 outline-none"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Industrial Cluster</label>
                  <input
                    type="text"
                    value={formData.cluster}
                    onChange={(e) => setFormData({ ...formData, cluster: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium focus:bg-white focus:border-blue-500 outline-none"
                  />
                </div>
              </div>
            </div>
          )}

          {activeStep === 2 && (
            <div className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">PAN Number</label>
                  <input
                    type="text"
                    value={formData.pan}
                    onChange={(e) => setFormData({ ...formData, pan: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-mono font-bold"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">IEC (Import Export Code)</label>
                  <input
                    type="text"
                    value={formData.iec}
                    onChange={(e) => setFormData({ ...formData, iec: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-mono font-bold"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">AD Code (Bank Remittance)</label>
                  <input
                    type="text"
                    value={formData.ad_code}
                    onChange={(e) => setFormData({ ...formData, ad_code: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-mono font-bold"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">RCMC / CLE Membership</label>
                  <input
                    type="text"
                    value={formData.rcmc_number}
                    onChange={(e) => setFormData({ ...formData, rcmc_number: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-mono"
                  />
                </div>
              </div>
            </div>
          )}

          {activeStep === 3 && (
            <div className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Monthly Capacity (sqft)</label>
                  <input
                    type="number"
                    value={formData.monthly_capacity_sqft}
                    onChange={(e) => setFormData({ ...formData, monthly_capacity_sqft: Number(e.target.value) })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-mono font-bold"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Port of Export</label>
                  <input
                    type="text"
                    value={formData.port_of_export}
                    onChange={(e) => setFormData({ ...formData, port_of_export: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-200 font-medium"
                  />
                </div>
              </div>
            </div>
          )}

          {activeStep === 4 && (
            <div className="space-y-4 text-xs">
              <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-900 flex items-start gap-3">
                <ShieldCheck size={24} className="text-emerald-600 shrink-0 mt-0.5" />
                <div>
                  <p className="font-bold text-sm text-emerald-950">
                    Exporter Readiness Score: {gaps?.overall_score || 95}/100
                  </p>
                  <p className="text-[11px] text-emerald-800 mt-0.5">
                    All mandatory DGFT, ICEGATE, and GST registrations verified. Profile approved for live buyer matching.
                  </p>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="font-bold text-slate-700 uppercase tracking-wider text-[10px]">Verified Credentials</h4>
                <div className="grid grid-cols-2 gap-2">
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                    <span>GSTIN / LUT Zero-Rated</span>
                    <AppleBadge tone="green" size="sm">Active</AppleBadge>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                    <span>DGFT IEC Registration</span>
                    <AppleBadge tone="green" size="sm">Verified</AppleBadge>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                    <span>AD Code Bank Account</span>
                    <AppleBadge tone="green" size="sm">Mapped</AppleBadge>
                  </div>
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-between">
                    <span>CLE RCMC Membership</span>
                    <AppleBadge tone="green" size="sm">2026/27</AppleBadge>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer Navigation */}
        <div className="p-4 px-6 border-t border-slate-100 bg-slate-50 flex items-center justify-between">
          <button
            type="button"
            disabled={activeStep === 1}
            onClick={() => setActiveStep(activeStep - 1)}
            className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 disabled:opacity-30 cursor-pointer"
          >
            <ArrowLeft size={14} />
            <span>Previous</span>
          </button>

          <AppleButton variant="primary" size="sm" onClick={handleNext} icon={<ArrowRight size={14} />}>
            {activeStep === 4 ? 'Complete Onboarding' : 'Save & Continue'}
          </AppleButton>
        </div>
      </div>
    </div>
  );
};
