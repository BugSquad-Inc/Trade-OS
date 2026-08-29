import React, { useState } from 'react';
import { QrCode, ShieldCheck, Tag, FileText, CheckCircle, Plus, ChevronRight, Layers, ArrowUpRight } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useProducts, ProductFamily, ProductVersion } from '../../api/products';

export const ProductPassportView: React.FC = () => {
  const { data: products, isLoading } = useProducts();
  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);

  if (isLoading) {
    return <PageSkeleton />;
  }

  const productList = products || [];
  const activeProduct = productList.find((p) => p.id === selectedProductId) || productList[0];
  const activeVersion = activeProduct?.versions?.[0];
  const activePassport = activeVersion?.passports?.[0];

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-600 text-white shadow-lg shadow-blue-500/10">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="text-xl font-bold tracking-tight">Digital Product Passports & Catalog</h2>
            <span className="px-2 py-0.5 rounded-full bg-white/20 text-white text-[11px] font-medium backdrop-blur-md">
              EU DPP Standard Ready
            </span>
          </div>
          <p className="text-xs text-blue-100 mt-1 max-w-xl font-medium">
            Version-controlled leather specifications with immutable lab test verifications and EU trade requirement clearance.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <AppleButton
            variant="secondary"
            size="sm"
            className="bg-white/15 text-white hover:bg-white/25 border-white/20"
            icon={<Plus size={14} />}
          >
            New Product Family
          </AppleButton>
        </div>
      </div>

      {productList.length === 0 ? (
        <EmptyState title="No Product Passports Found" description="Register a product family to generate your first Digital Product Passport." />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Product List */}
          <div className="space-y-3 lg:col-span-1">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">Registered Product Families</h3>
            {productList.map((product) => {
              const isSelected = product.id === activeProduct?.id;
              const version = product.versions?.[0];
              return (
                <AppleCard
                  key={product.id}
                  variant={isSelected ? 'elevated' : 'default'}
                  onClick={() => setSelectedProductId(product.id)}
                  className={`cursor-pointer transition-all ${
                    isSelected ? 'border-blue-400 ring-2 ring-blue-500/20 bg-blue-50/40' : 'hover:border-slate-300'
                  }`}
                >
                  <div className="space-y-2">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="text-sm font-bold text-slate-900 tracking-tight">{product.name}</h4>
                      <AppleBadge tone="blue" size="sm">HS {product.hs_code}</AppleBadge>
                    </div>
                    <p className="text-xs text-slate-500 line-clamp-2">{product.description}</p>
                    <div className="flex items-center justify-between pt-2 border-t border-slate-200/70 text-[11px] text-slate-600">
                      <span>{product.leather_type}</span>
                      {version && (
                        <span className="font-bold text-slate-900 font-mono">₹{version.price_basis_inr}/sqft (${version.price_basis_usd})</span>
                      )}
                    </div>
                  </div>
                </AppleCard>
              );
            })}
          </div>

          {/* Right: Active Digital Product Passport Card */}
          {activeProduct && activeVersion && (
            <div className="space-y-5 lg:col-span-2">
              <AppleCard variant="default" className="space-y-6 bg-white border-slate-200/90 shadow-sm">
                {/* Passport Header */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-5 border-b border-slate-100">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="text-lg font-bold text-slate-900">{activeProduct.name}</h3>
                      <AppleBadge tone="green" size="sm" dot>Passport Active</AppleBadge>
                      <TruthStatusBadge status="verified" sourceName="Audited Lab Tests" />
                    </div>
                    <p className="text-xs font-mono text-slate-400">
                      Passport ID: <b className="text-slate-700">{activePassport?.passport_number || 'DPP-IN-ACTIVE'}</b> · ITC(HS): {activeProduct.itc_hs_code}
                    </p>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <div className="p-3 rounded-2xl bg-slate-50 border border-slate-200 text-slate-700 flex items-center gap-2">
                      <QrCode size={24} className="text-slate-800" />
                      <div className="text-left">
                        <p className="text-[9px] font-bold uppercase text-slate-400">Buyer Scan</p>
                        <p className="text-[10px] font-bold text-emerald-700">QR Validated</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Technical Specifications Grid */}
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Technical Specifications ({activeVersion.version_tag})</h4>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Thickness</span>
                      <p className="font-semibold text-slate-900 font-mono">{activeVersion.thickness_range_mm.join(', ')} mm</p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Monthly Capacity</span>
                      <p className="font-semibold text-slate-900 font-mono">{activeVersion.monthly_capacity_sqft.toLocaleString()} sqft</p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">MOQ</span>
                      <p className="font-semibold text-slate-900 font-mono">{activeVersion.moq_sqft.toLocaleString()} sqft</p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Lead Time</span>
                      <p className="font-semibold text-slate-900 font-mono">{activeVersion.lead_time_days} days (Air: {activeVersion.sample_lead_time_days}d)</p>
                    </div>
                  </div>
                </div>

                {/* Commercial Pricing & Incoterms */}
                <div className="p-4 rounded-2xl bg-gradient-to-r from-slate-50 to-blue-50/40 border border-slate-200/90 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">FOB Reference Price</span>
                    <div className="flex items-baseline gap-2">
                      <span className="text-xl font-bold font-mono text-slate-900">₹{activeVersion.price_basis_inr}</span>
                      <span className="text-xs font-semibold text-slate-500 font-mono">(${activeVersion.price_basis_usd} USD/sqft)</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500 font-medium">Incoterms:</span>
                    {activeVersion.incoterms.map((inc, i) => (
                      <span key={i} className="px-2 py-0.5 rounded-lg bg-white border border-slate-200 text-slate-700 text-xs font-semibold shadow-2xs">
                        {inc}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Attached Lab Test & Environmental Certificates */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                      Verified Lab Test & Compliance Certificates ({activeVersion.certificates.length})
                    </h4>
                  </div>

                  <div className="space-y-2">
                    {activeVersion.certificates.map((cert) => (
                      <div
                        key={cert.id}
                        className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 gap-3 text-xs"
                      >
                        <div className="flex items-start gap-3">
                          <div className="p-2 rounded-lg bg-emerald-100 text-emerald-700 shrink-0 mt-0.5">
                            <ShieldCheck size={16} />
                          </div>
                          <div>
                            <div className="flex items-center gap-2 flex-wrap">
                              <h5 className="font-bold text-slate-900">{cert.certificate_name}</h5>
                              <AppleBadge tone="green" size="sm">{cert.cert_type}</AppleBadge>
                            </div>
                            <p className="text-[11px] text-slate-500 mt-0.5">
                              Lab: <b>{cert.accredited_lab}</b> · Issued by: {cert.issuer}
                            </p>
                          </div>
                        </div>

                        <div className="flex items-center gap-3 shrink-0 text-right sm:text-right w-full sm:w-auto justify-between sm:justify-end border-t sm:border-0 pt-2 sm:pt-0 border-slate-200">
                          <div className="text-[10px] text-slate-500">
                            Valid until: <b className="text-slate-800">{cert.expiry_date || 'Perpetual'}</b>
                          </div>
                          <span className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 font-bold border border-emerald-200 text-[10px]">
                            Verified
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </AppleCard>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
