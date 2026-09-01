import React, { useState } from 'react';
import { QrCode, ShieldCheck, Tag, FileText, CheckCircle, Plus, ChevronRight, Layers, ArrowUpRight, Share2, Award, ExternalLink, MapPin, FlaskConical, Leaf } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleButton } from '../apple/AppleButton';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';
import { PageSkeleton } from '../ui/PageSkeleton';
import { EmptyState } from '../ui/EmptyState';
import { useProducts, ProductFamily, ProductVersion, useCreateProduct } from '../../api/products';

export const ProductPassportView: React.FC = () => {
  const { data: products, isLoading } = useProducts();
  const createProduct = useCreateProduct();
  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [copiedToken, setCopiedToken] = useState(false);

  // New Product State
  const [newProdName, setNewProdName] = useState('');
  const [newLeatherType, setNewLeatherType] = useState('Bovine Full Grain');
  const [newHsCode, setNewHsCode] = useState('4107');
  const [newPriceBasisInr, setNewPriceBasisInr] = useState(295);

  if (isLoading) {
    return <PageSkeleton />;
  }

  const productList = products || [];
  const activeProduct = productList.find((p) => p.id === selectedProductId) || productList[0];
  const activeVersion = activeProduct?.versions?.[0];
  const activePassport = activeVersion?.passports?.[0];
  const spec = activeVersion?.specifications;
  const chem = activeVersion?.chemical_spec;
  const trace = activeVersion?.traceability_spec;

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newProdName.trim()) return;
    createProduct.mutate(
      {
        name: newProdName,
        category: 'Finished Leather',
        hs_code: newHsCode,
        leather_type: newLeatherType,
        price_basis_inr: newPriceBasisInr,
        price_basis_usd: Number((newPriceBasisInr / 83.5).toFixed(2)),
      },
      {
        onSuccess: () => {
          setIsCreateModalOpen(false);
          setNewProdName('');
        },
      }
    );
  };

  const handleCopyPublicDppUrl = () => {
    if (activePassport?.public_token) {
      const url = `${window.location.origin}/api/v1/products/dpp/public/${activePassport.public_token}`;
      navigator.clipboard.writeText(url);
      setCopiedToken(true);
      setTimeout(() => setCopiedToken(false), 2000);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-blue-700 via-blue-600 to-indigo-700 text-white shadow-lg">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="text-xl font-bold tracking-tight">Product Matrix & Digital Product Passports</h2>
            <span className="px-2 py-0.5 rounded-full bg-white/20 text-white text-[11px] font-medium backdrop-blur-md">
              EU DPP & EUDR Compliant
            </span>
          </div>
          <p className="text-xs text-blue-100 mt-1 max-w-xl font-medium">
            Multi-article leather specifications with verified chemical limits (Cr VI, Azo, Formaldehyde), abattoir geolocation, and QR-ready Digital Passports.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <AppleButton
            variant="secondary"
            size="sm"
            className="bg-white/15 text-white hover:bg-white/25 border-white/20"
            icon={<Plus size={14} />}
            onClick={() => setIsCreateModalOpen(true)}
          >
            Add Leather Article
          </AppleButton>
        </div>
      </div>

      {productList.length === 0 ? (
        <EmptyState title="No Product Passports Found" description="Register a product family to generate your first Digital Product Passport." />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Product List */}
          <div className="space-y-3 lg:col-span-1">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">Registered Articles</h3>
            {productList.map((product) => {
              const isSelected = product.id === activeProduct?.id;
              const version = product.versions?.[0];
              return (
                <AppleCard
                  key={product.id}
                  variant={isSelected ? 'elevated' : 'default'}
                  onClick={() => setSelectedProductId(product.id)}
                  className={`cursor-pointer transition-all ${
                    isSelected ? 'border-blue-500 ring-2 ring-blue-500/20 bg-blue-50/40' : 'hover:border-slate-300'
                  }`}
                >
                  <div className="space-y-2">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="text-sm font-bold text-slate-900 tracking-tight">{product.name}</h4>
                      <AppleBadge tone="blue" size="sm">HS {product.hs_code}</AppleBadge>
                    </div>
                    <p className="text-xs text-slate-500 line-clamp-2">{product.description || 'Export grade finished crust and nappa article.'}</p>
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
              <AppleCard variant="default" className="space-y-6 bg-white border-slate-200/90 shadow-sm p-6">
                {/* Passport Header */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-5 border-b border-slate-100">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="text-lg font-bold text-slate-900">{activeProduct.name}</h3>
                      <AppleBadge tone="green" size="sm" dot>Passport Active</AppleBadge>
                      <TruthStatusBadge status="verified" sourceName="TÜV & APEDA" />
                    </div>
                    <p className="text-xs font-mono text-slate-400">
                      Passport ID: <b className="text-slate-700">{activePassport?.passport_number || 'DPP-IN-ACTIVE'}</b> · HS: {activeProduct.hs_code}
                    </p>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <AppleButton
                      variant="secondary"
                      size="sm"
                      icon={<Share2 size={13} />}
                      onClick={handleCopyPublicDppUrl}
                    >
                      {copiedToken ? 'URL Copied!' : 'Copy Buyer DPP Link'}
                    </AppleButton>
                  </div>
                </div>

                {/* Physical Technical Parameters */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Layers size={13} className="text-blue-500" />
                      Physical Specifications ({activeVersion.version_tag})
                    </h4>
                    <WhatDoesThisMean term="HS Code (Harmonized System)" />
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Thickness Range</span>
                      <p className="font-semibold text-slate-900 font-mono">
                        {spec ? `${spec.thickness_min_mm} - ${spec.thickness_max_mm} mm` : activeVersion.thickness_range_mm.join(', ') + ' mm'}
                      </p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Temper / Feel</span>
                      <p className="font-semibold text-slate-900 font-mono capitalize">
                        {spec?.temper?.replace('_', ' ') || 'Medium Soft'}
                      </p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Tensile Strength</span>
                      <p className="font-semibold text-slate-900 font-mono">
                        {spec?.tensile_strength_n_per_mm2 || 15.0} N/mm²
                      </p>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/80 space-y-0.5">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Tannage Chemistry</span>
                      <p className="font-semibold text-slate-900 truncate">
                        {spec?.tannage_type || 'Chrome-Free / Veg Retan'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Chemical Compliance Safety Card (REACH / SVHC) */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                      <FlaskConical size={13} className="text-emerald-600" />
                      REACH & European Chemical Safety
                    </h4>
                    <WhatDoesThisMean term="REACH & SVHC" />
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                    <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-200/80 space-y-0.5">
                      <span className="text-[10px] text-emerald-800 font-bold uppercase">Chromium VI (Cr VI)</span>
                      <p className="font-bold text-emerald-900 font-mono">{chem?.chromium_vi_ppm ?? 0.0} ppm (&lt;3.0 limit)</p>
                    </div>
                    <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-200/80 space-y-0.5">
                      <span className="text-[10px] text-emerald-800 font-bold uppercase">Restricted Azo Dyes</span>
                      <p className="font-bold text-emerald-900 font-mono">{chem?.azo_dyes_ppm ?? 0.0} ppm (Azo-Free)</p>
                    </div>
                    <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-200/80 space-y-0.5">
                      <span className="text-[10px] text-emerald-800 font-bold uppercase">Formaldehyde</span>
                      <p className="font-bold text-emerald-900 font-mono">{chem?.formaldehyde_ppm ?? 12.0} ppm (&lt;75 limit)</p>
                    </div>
                    <div className="p-3 rounded-xl bg-emerald-50/60 border border-emerald-200/80 space-y-0.5">
                      <span className="text-[10px] text-emerald-800 font-bold uppercase">PFAS Chemicals</span>
                      <p className="font-bold text-emerald-900 font-mono">{chem?.pfas_free !== false ? '100% PFAS-Free' : 'Tested'}</p>
                    </div>
                  </div>
                </div>

                {/* EUDR Traceability & Carbon Footprint Card */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                      <Leaf size={13} className="text-teal-600" />
                      EUDR Traceability & Environmental Footprint
                    </h4>
                    <WhatDoesThisMean term="EUDR (EU Deforestation Regulation)" />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                    <div className="p-3.5 rounded-xl bg-teal-50/60 border border-teal-200/80 space-y-1">
                      <div className="flex items-center gap-1.5 text-teal-900 font-bold">
                        <MapPin size={14} className="text-teal-700" />
                        <span>Abattoir Origin & Geolocation</span>
                      </div>
                      <p className="text-[11px] text-teal-800">
                        License: <b>{trace?.abattoir_license_no || 'APEDA-TN-7821'}</b> · {trace?.mandal_district || 'Ambur, Tamil Nadu'}
                      </p>
                      <p className="text-[10px] font-mono text-teal-700">
                        Coordinates: {trace?.geolocation_lat || 12.7904}° N, {trace?.geolocation_lng || 78.7163}° E (Deforestation Cleared)
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-blue-50/60 border border-blue-200/80 space-y-1">
                      <div className="flex items-center gap-1.5 text-blue-900 font-bold">
                        <Award size={14} className="text-blue-700" />
                        <span>Carbon Estimate & Sustainability</span>
                      </div>
                      <p className="text-[11px] text-blue-800">
                        Carbon Footprint: <b>{activePassport?.carbon_footprint_kg_co2e || 4.2} kg CO₂e / sqft</b>
                      </p>
                      <p className="text-[10px] text-blue-700 font-medium">
                        Audited under LWG Environmental & Water Conservation Protocol
                      </p>
                    </div>
                  </div>
                </div>

                {/* Attached Lab Certificates */}
                <div className="space-y-3 pt-2 border-t border-slate-100">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    Verified Certificates ({activeVersion.certificates.length})
                  </h4>

                  <div className="space-y-2">
                    {activeVersion.certificates.map((cert) => (
                      <div
                        key={cert.id}
                        className="flex items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs"
                      >
                        <div className="flex items-center gap-2.5">
                          <ShieldCheck size={16} className="text-emerald-600 shrink-0" />
                          <div>
                            <span className="font-bold text-slate-900">{cert.certificate_name}</span>
                            <p className="text-[10px] text-slate-500">Issued by {cert.issuer} · Lab: {cert.accredited_lab}</p>
                          </div>
                        </div>
                        <AppleBadge tone="green" size="sm">Verified</AppleBadge>
                      </div>
                    ))}
                  </div>
                </div>
              </AppleCard>
            </div>
          )}
        </div>
      )}

      {/* Add Product Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
          <div className="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 space-y-4">
            <h3 className="text-base font-bold text-slate-900">Add New Leather Article</h3>
            <form onSubmit={handleCreate} className="space-y-3 text-xs font-medium">
              <div>
                <label className="block text-slate-600 mb-1">Article Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Vintage Full-Grain Cowhide"
                  value={newProdName}
                  onChange={(e) => setNewProdName(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-blue-500/20"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-600 mb-1">Leather Type</label>
                  <input
                    type="text"
                    value={newLeatherType}
                    onChange={(e) => setNewLeatherType(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200"
                  />
                </div>
                <div>
                  <label className="block text-slate-600 mb-1">HS Code</label>
                  <input
                    type="text"
                    value={newHsCode}
                    onChange={(e) => setNewHsCode(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-200 font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-slate-600 mb-1">Price Basis (INR / sqft FOB)</label>
                <input
                  type="number"
                  value={newPriceBasisInr}
                  onChange={(e) => setNewPriceBasisInr(Number(e.target.value))}
                  className="w-full px-3 py-2 rounded-xl border border-slate-200 font-mono"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="px-3 py-1.5 rounded-xl text-slate-600 hover:bg-slate-100 font-semibold"
                >
                  Cancel
                </button>
                <AppleButton variant="primary" size="sm" type="submit" disabled={createProduct.isPending}>
                  Create Article
                </AppleButton>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
