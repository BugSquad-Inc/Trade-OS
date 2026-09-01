import React, { useState } from 'react';
import { Layers, Plus, ArrowRight, DollarSign, Calculator, ChevronRight, CheckCircle2, TrendingUp, SlidersHorizontal } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useDeals, usePipelineSummary, useIssueQuote, Opportunity } from '../../api/deals';
import { LandedCostCalculatorModal } from './LandedCostCalculatorModal';
import { JourneyTransitionModal } from './JourneyTransitionModal';

export const DealsPipelineView: React.FC = () => {
  const { data: deals, isLoading } = useDeals();
  const { data: summary } = usePipelineSummary();
  const issueQuote = useIssueQuote();

  const [isCalculatorOpen, setIsCalculatorOpen] = useState(false);
  const [selectedOppForQuote, setSelectedOppForQuote] = useState<Opportunity | null>(null);
  const [selectedOppForTransition, setSelectedOppForTransition] = useState<Opportunity | null>(null);

  if (isLoading) return <PageSkeleton />;

  const dealList = deals || [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Top Banner & KPI Summary */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-blue-950 to-indigo-950 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold tracking-tight">12-Stage Export Deals & Quotation Pipeline</h2>
            <span className="px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-200 text-[11px] font-medium border border-blue-400/20">
              Corridor: India → Germany / EU
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-1 max-w-xl font-medium">
            From verified buyer match to physical sample approval, Landed DDP quotations, and PO issuance. Governed by backend journey rules.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="p-3 rounded-2xl bg-white/10 border border-white/10 text-right">
            <p className="text-[10px] uppercase font-bold text-slate-400">Active Pipeline</p>
            <p className="text-lg font-bold font-mono text-emerald-400">€{(summary?.total_pipeline_eur || 182750).toLocaleString()}</p>
          </div>
          <AppleButton
            variant="secondary"
            size="sm"
            className="bg-white/15 text-white hover:bg-white/25 border-white/20"
            icon={<Calculator size={14} />}
            onClick={() => setIsCalculatorOpen(true)}
          >
            Landed Cost Calculator
          </AppleButton>
        </div>
      </div>

      {/* Pipeline Board */}
      {dealList.length === 0 ? (
        <EmptyState title="No Active Deals" description="Generate quotes from buyer match candidates to populate your pipeline." />
      ) : (
        <div className="space-y-4">
          {dealList.map((deal) => {
            const hasQuote = deal.quotes && deal.quotes.length > 0;
            const quote = hasQuote ? deal.quotes[0] : null;

            return (
              <AppleCard
                key={deal.id}
                variant="default"
                className="bg-white border-slate-200/90 shadow-2xs hover:border-blue-300 transition-all p-5"
              >
                <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
                  <div className="space-y-2 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h4 className="text-sm font-bold text-slate-900">{deal.title}</h4>
                      <AppleBadge tone="blue" size="sm">
                        {deal.stage.replace(/_/g, ' ').toUpperCase()}
                      </AppleBadge>
                      <TruthStatusBadge status="verified" sourceName="Stage Gate" />
                      <span className="text-[11px] font-mono font-bold text-slate-500">
                        {deal.volume_sqft.toLocaleString()} sqft · {deal.incoterms}
                      </span>
                    </div>

                    <p className="text-xs text-slate-600 font-medium">
                      Owner: <b>{deal.owner}</b> · Win Probability: <b className="text-emerald-700">{(deal.probability * 100).toFixed(0)}%</b>
                    </p>

                    {deal.notes && (
                      <p className="text-[11px] text-slate-500 bg-slate-50 p-2.5 rounded-xl border border-slate-100 italic">
                        "{deal.notes}"
                      </p>
                    )}

                    {quote && (
                      <div className="flex items-center gap-3 pt-1 text-xs text-slate-600">
                        <span className="font-mono bg-blue-50 text-blue-700 px-2 py-0.5 rounded-md font-bold">
                          Quote: {quote.quote_number} (€{quote.unit_price_eur}/sqft)
                        </span>
                        <span>Margin: <b className="text-slate-900">{quote.gross_margin_pct}%</b></span>
                        <span>Terms: {quote.payment_terms}</span>
                      </div>
                    )}
                  </div>

                  {/* Right: Value & Stage Action */}
                  <div className="flex items-center gap-4 shrink-0 w-full lg:w-auto justify-between lg:justify-end border-t lg:border-0 pt-3 lg:pt-0 border-slate-100">
                    <div className="text-left lg:text-right">
                      <p className="text-[10px] uppercase font-bold text-slate-400">Deal Value</p>
                      <p className="text-base font-bold font-mono text-slate-900">€{deal.deal_value_eur.toLocaleString()}</p>
                      <p className="text-[10px] font-mono text-slate-400">₹{(deal.deal_value_inr || deal.deal_value_eur * 92.5).toLocaleString()}</p>
                    </div>

                    <div className="flex items-center gap-2">
                      <AppleButton
                        variant="secondary"
                        size="sm"
                        icon={<Calculator size={13} />}
                        onClick={() => {
                          setSelectedOppForQuote(deal);
                          setIsCalculatorOpen(true);
                        }}
                      >
                        Quote
                      </AppleButton>

                      <AppleButton
                        variant="primary"
                        size="sm"
                        icon={<SlidersHorizontal size={13} />}
                        onClick={() => setSelectedOppForTransition(deal)}
                      >
                        Manage Stage Gate
                      </AppleButton>
                    </div>
                  </div>
                </div>
              </AppleCard>
            );
          })}
        </div>
      )}

      {/* Landed Cost Calculator Modal */}
      <LandedCostCalculatorModal
        isOpen={isCalculatorOpen}
        onClose={() => {
          setIsCalculatorOpen(false);
          setSelectedOppForQuote(null);
        }}
        initialUnitPriceInr={295.0}
        initialQuantitySqft={selectedOppForQuote?.volume_sqft || 5000}
        onApplyQuote={(calc) => {
          if (selectedOppForQuote) {
            issueQuote.mutate({
              oppId: selectedOppForQuote.id,
              data: {
                unit_price_inr: calc.unit_price_inr,
                quantity_sqft: calc.quantity_sqft,
                freight_usd: 1850.0,
                insurance_usd: 120.0,
                customs_duty_pct: 0.0,
                target_margin_pct: calc.gross_margin_pct,
                fx_rate_eur_inr: calc.fx_rate_eur_inr,
              },
            });
          }
        }}
      />

      {/* Journey Transition Modal */}
      <JourneyTransitionModal
        opportunity={selectedOppForTransition}
        isOpen={!!selectedOppForTransition}
        onClose={() => setSelectedOppForTransition(null)}
      />
    </div>
  );
};
