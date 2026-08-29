import React, { useState, useEffect } from 'react';
import { Calculator, ArrowRight, X, TrendingUp, ShieldCheck, DollarSign } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { useCalculateLandedCost, LandedCostCalculation } from '../../api/deals';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  initialUnitPriceInr?: number;
  initialQuantitySqft?: number;
  onApplyQuote?: (calc: LandedCostCalculation) => void;
}

export const LandedCostCalculatorModal: React.FC<Props> = ({
  isOpen,
  onClose,
  initialUnitPriceInr = 295.0,
  initialQuantitySqft = 5000,
  onApplyQuote,
}) => {
  const calculateMutation = useCalculateLandedCost();

  const [unitPriceInr, setUnitPriceInr] = useState<number>(initialUnitPriceInr);
  const [quantitySqft, setQuantitySqft] = useState<number>(initialQuantitySqft);
  const [freightUsd, setFreightUsd] = useState<number>(1850.0);
  const [insuranceUsd, setInsuranceUsd] = useState<number>(120.0);
  const [customsDutyPct, setCustomsDutyPct] = useState<number>(0.0);
  const [targetMarginPct, setTargetMarginPct] = useState<number>(25.0);
  const [fxRate, setFxRate] = useState<number>(92.5);

  const [result, setResult] = useState<LandedCostCalculation | null>(null);

  useEffect(() => {
    if (isOpen) {
      calculateMutation.mutate(
        {
          unit_price_inr: unitPriceInr,
          quantity_sqft: quantitySqft,
          freight_usd: freightUsd,
          insurance_usd: insuranceUsd,
          customs_duty_pct: customsDutyPct,
          target_margin_pct: targetMarginPct,
          fx_rate_eur_inr: fxRate,
        },
        {
          onSuccess: (data) => setResult(data),
        }
      );
    }
  }, [isOpen, unitPriceInr, quantitySqft, freightUsd, insuranceUsd, customsDutyPct, targetMarginPct, fxRate]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs" onClick={onClose} />
      <div className="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden z-50 flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-white/20">
              <Calculator size={20} />
            </div>
            <div>
              <h3 className="text-lg font-bold tracking-tight">Landed Cost & FX Margin Calculator</h3>
              <p className="text-xs text-blue-100 font-medium">INR Ex-Factory to European Port DDP/CIF Pricing</p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/20 cursor-pointer"
          >
            <X size={18} />
          </button>
        </div>

        {/* Form & Results Grid */}
        <div className="p-6 overflow-y-auto space-y-5 flex-1">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            {/* Left: Input Parameters */}
            <div className="space-y-3 bg-slate-50 p-4 rounded-2xl border border-slate-200">
              <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">Cost & Volume Inputs</h4>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Ex-Factory FOB Price (₹ INR / sqft)</label>
                <input
                  type="number"
                  value={unitPriceInr}
                  onChange={(e) => setUnitPriceInr(Number(e.target.value))}
                  className="w-full px-3 py-2 rounded-xl bg-white border border-slate-300 font-mono font-bold focus:border-blue-500 outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Order Volume (sqft)</label>
                  <input
                    type="number"
                    value={quantitySqft}
                    onChange={(e) => setQuantitySqft(Number(e.target.value))}
                    className="w-full px-3 py-2 rounded-xl bg-white border border-slate-300 font-mono"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">EUR/INR FX Rate</label>
                  <input
                    type="number"
                    step="0.1"
                    value={fxRate}
                    onChange={(e) => setFxRate(Number(e.target.value))}
                    className="w-full px-3 py-2 rounded-xl bg-white border border-slate-300 font-mono"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Freight ($ USD)</label>
                  <input
                    type="number"
                    value={freightUsd}
                    onChange={(e) => setFreightUsd(Number(e.target.value))}
                    className="w-full px-3 py-2 rounded-xl bg-white border border-slate-300 font-mono"
                  />
                </div>
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Target Margin %</label>
                  <input
                    type="number"
                    value={targetMarginPct}
                    onChange={(e) => setTargetMarginPct(Number(e.target.value))}
                    className="w-full px-3 py-2 rounded-xl bg-white border border-slate-300 font-mono font-bold text-blue-600"
                  />
                </div>
              </div>
            </div>

            {/* Right: Real-time Calculation Result */}
            {result && (
              <div className="space-y-3 bg-gradient-to-br from-slate-900 to-indigo-950 text-white p-5 rounded-2xl shadow-md flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between border-b border-white/10 pb-3 mb-3">
                    <span className="text-[11px] font-bold text-slate-300 uppercase tracking-wider">Recommended Quote</span>
                    <AppleBadge tone="green" size="sm">Margin: {result.gross_margin_pct}%</AppleBadge>
                  </div>

                  <div className="space-y-1">
                    <span className="text-xs text-slate-400 font-medium">Selling Price (CIF European Port)</span>
                    <div className="flex items-baseline gap-2">
                      <span className="text-3xl font-extrabold font-mono text-white">€{result.recommended_unit_price_eur}</span>
                      <span className="text-xs text-slate-300 font-mono">/ sqft</span>
                    </div>
                  </div>

                  <div className="mt-4 space-y-1.5 text-xs text-slate-300 border-t border-white/10 pt-3">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Base Cost (EUR):</span>
                      <span className="font-mono text-white">€{result.base_eur_per_sqft}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Ocean Freight + Ins:</span>
                      <span className="font-mono text-white">€{(result.freight_eur_per_sqft + result.insurance_eur_per_sqft).toFixed(3)}</span>
                    </div>
                    <div className="flex justify-between border-t border-white/10 pt-1 font-semibold">
                      <span className="text-slate-300">Total Landed Cost:</span>
                      <span className="font-mono text-emerald-400">€{result.landed_cost_eur_per_sqft} / sqft</span>
                    </div>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-white/10 border border-white/10 space-y-1 mt-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300">Total Contract (EUR):</span>
                    <span className="font-bold font-mono text-white">€{result.total_quote_value_eur.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-300">Total Realization (INR):</span>
                    <span className="font-bold font-mono text-emerald-400">₹{result.total_quote_value_inr.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 px-6 border-t border-slate-100 bg-slate-50 flex items-center justify-between">
          <AppleButton variant="secondary" size="sm" onClick={onClose}>
            Close
          </AppleButton>
          {onApplyQuote && result && (
            <AppleButton
              variant="primary"
              size="sm"
              icon={<ArrowRight size={14} />}
              onClick={() => {
                onApplyQuote(result);
                onClose();
              }}
            >
              Apply to Deal Quotation
            </AppleButton>
          )}
        </div>
      </div>
    </div>
  );
};
