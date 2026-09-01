import React, { useState } from 'react';
import { X, Search, BookOpen, ExternalLink, HelpCircle, ShieldCheck } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';
import { AppleBadge } from '../apple/AppleBadge';

interface GlossaryEntry {
  term: string;
  category: 'Compliance' | 'Trade Finance' | 'Logistics' | 'Product Specs' | 'Truth & Data';
  shortDef: string;
  fullExplanation: string;
  indianContext: string;
  actionableTip: string;
}

const GLOSSARY_ENTRIES: GlossaryEntry[] = [
  {
    term: 'eBRC (Electronic Bank Realization Certificate)',
    category: 'Trade Finance',
    shortDef: 'Digital certificate issued by your bank confirming receipt of export foreign exchange.',
    fullExplanation: 'An eBRC is generated automatically by Indian AD (Authorized Dealer) banks and transmitted to DGFT. It serves as official legal proof that export proceeds were received into your Indian bank account.',
    indianContext: 'Mandatory for claiming Indian government export incentives (Duty Drawback, RoDTEP) and closing RBI EDPMS realization entries.',
    actionableTip: 'Ensure your CHA files the exact Inward Remittance / FIRC details matching the shipping bill to prevent eBRC generation delays.'
  },
  {
    term: 'EUDR (EU Deforestation Regulation)',
    category: 'Compliance',
    shortDef: 'European regulation requiring proof that raw hides did not originate from deforested land after 31 Dec 2020.',
    fullExplanation: 'Under EUDR, EU leather buyers cannot import bovine products unless their suppliers provide farm/aggregator geolocation coordinates (polygon/point data) and proof of legal land use.',
    indianContext: 'Critical for Chennai & Ambur tanneries exporting finished bovine leather to Germany, Italy, and France.',
    actionableTip: 'Maintain raw hide purchase traceability sheets with abattoir and mandal geolocation records in your Trade OS Document Vault.'
  },
  {
    term: 'REACH & SVHC',
    category: 'Compliance',
    shortDef: 'European chemical safety standards banning dangerous substances like Hexavalent Chromium (Cr VI) and Azo dyes.',
    fullExplanation: 'REACH (Registration, Evaluation, Authorisation and Restriction of Chemicals) regulates harmful chemical limits in imported consumer goods. SVHC (Substances of Very High Concern) lists candidate chemicals requiring strict declaration.',
    indianContext: 'German luxury brands (Bader, Hugo Boss, Roeckl) mandate third-party lab test reports (SGS, TUV, Eurofins) showing zero Cr VI (<3 mg/kg) and no restricted Azo amines.',
    actionableTip: 'Upload your latest 90-day tannery batch test report to your Digital Product Passport before sending quotes.'
  },
  {
    term: 'LWG (Leather Working Group)',
    category: 'Compliance',
    shortDef: 'Global environmental standard auditing energy, water, chemical usage, and worker safety in tanneries.',
    fullExplanation: 'LWG rates tanneries as Gold, Silver, Bronze, or Audited. More than 80% of top EU and US leather brands require minimum Silver or Gold rating for their Tier-1 and Tier-2 suppliers.',
    indianContext: 'Butler\'s Leather cluster in Ambur holds LWG Gold/Silver recognition, providing a strong competitive edge over non-audited regional suppliers.',
    actionableTip: 'Highlight your LWG medal and valid audit expiry date directly in buyer outreach emails.'
  },
  {
    term: 'Digital Product Passport (DPP)',
    category: 'Product Specs',
    shortDef: 'A digital, QR-accessible technical datasheet containing material specs, compliance tests, and origin proof.',
    fullExplanation: 'The European Union Ecodesign framework requires products to carry a digital identity detailing origin, tannage chemistry, carbon footprint, and recyclability.',
    indianContext: 'Replaces messy PDF email attachments. Indian exporters can send a secure Trade OS link that EU buyers can inspect in one click.',
    actionableTip: 'Generate a DPP QR code for your sample swatches before dispatching swatch kits to Frankfurt or Hamburg.'
  },
  {
    term: 'Incoterms (FOB, CIF, EXW, DAP)',
    category: 'Logistics',
    shortDef: 'Standard 3-letter trade terms defining who pays for freight, insurance, and customs clearance.',
    fullExplanation: 'FOB (Free On Board Chennai) means you pay transport until goods are loaded on the ship at Chennai Port; buyer pays sea freight and EU import customs. CIF (Cost, Insurance & Freight Hamburg) means you pay ocean freight and marine insurance to Hamburg Port.',
    indianContext: 'For pilot orders with German buyers, FOB Chennai (INMAA) is recommended. Repeat volume orders can transition to CIF Hamburg (DEHAM) once freight benchmarks are locked.',
    actionableTip: 'Always check the live Trade OS Ocean Freight Benchmark before quoting CIF.'
  },
  {
    term: 'HS Code (Harmonized System)',
    category: 'Product Specs',
    shortDef: 'International 6-to-8 digit customs code used by customs authorities globally to classify goods.',
    fullExplanation: 'Chapter 41 covers raw hides, skins, and leather. HS 4104 is tanned bovine leather, HS 4106 is goat/kid leather, and HS 4107 is finished leather further prepared after tanning (full-grain, split, upholstery).',
    indianContext: 'Selecting the exact 8-digit HS code on Indian Shipping Bills determines correct export duty drawback and GST refund eligibility.',
    actionableTip: 'Use Trade OS Buyer Matcher to automatically align your product with the buyer\'s historical import HS codes.'
  },
  {
    term: 'Duty Drawback & RoDTEP',
    category: 'Trade Finance',
    shortDef: 'Indian government tax refund schemes returning embedded customs duties and state taxes to exporters.',
    fullExplanation: 'Duty Drawback refunds import duties paid on imported tanning chemicals. RoDTEP (Remission of Duties and Taxes on Exported Products) refunds un-rebated central and state electricity/fuel taxes.',
    indianContext: 'Provides 1.5% to 3.5% additional export revenue realization for finished leather products.',
    actionableTip: 'Trade OS Money Hub automatically estimates your receivable RoDTEP and Drawback on every generated quotation.'
  },
  {
    term: 'Truth Status Badges',
    category: 'Truth & Data',
    shortDef: 'System badges indicating the exact verification pedigree and freshness of any data point in Trade OS.',
    fullExplanation: 'Trade OS categorizes all claims: Verified (proven by official documents), Exporter Declared (submitted by factory), Model Estimated (calculated via scoring algorithms), Rule Checked (passed software validation), Stale (>90 days old), or Demo (synthetic testing sample).',
    indianContext: 'Guarantees that Indian business owners never send unverified or misleading compliance claims to international buyers.',
    actionableTip: 'Hover over any truth badge to see its original data source, verified date, and validation authority.'
  }
];

export const ExportGlossaryModal: React.FC = () => {
  const { isGlossaryModalOpen, setGlossaryModalOpen, activeGlossaryTerm } = useUIStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  if (!isGlossaryModalOpen) return null;

  const categories = ['All', 'Compliance', 'Trade Finance', 'Logistics', 'Product Specs', 'Truth & Data'];

  const filteredEntries = GLOSSARY_ENTRIES.filter((entry) => {
    const matchesSearch =
      entry.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.shortDef.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.fullExplanation.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCat = selectedCategory === 'All' || entry.category === selectedCategory;
    return matchesSearch && matchesCat;
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs animate-in fade-in duration-150">
      <div className="relative w-full max-w-3xl max-h-[85vh] bg-white rounded-3xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200/80 bg-slate-50/80 shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
              <BookOpen size={18} />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-2">
                Trade OS Export Glossary
                <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700">
                  Plain English
                </span>
              </h2>
              <p className="text-xs text-slate-500 font-medium">
                Practical explanations of export terminology, compliance rules, and Indian trade incentives
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={() => setGlossaryModalOpen(false)}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div className="p-4 border-b border-slate-100 bg-white space-y-3 shrink-0">
          <div className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search export terms (e.g., eBRC, EUDR, FOB, REACH, RoDTEP)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all placeholder:text-slate-400 font-medium"
            />
          </div>

          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
            {categories.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setSelectedCategory(cat)}
                className={`px-2.5 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors cursor-pointer ${
                  selectedCategory === cat
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200/70'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4 divide-y divide-slate-100">
          {filteredEntries.length === 0 ? (
            <div className="text-center py-12 space-y-2">
              <p className="text-sm font-bold text-slate-700">No matching export term found</p>
              <p className="text-xs text-slate-500">Try searching for terms like "eBRC", "Incoterms", "EUDR", or "LWG"</p>
            </div>
          ) : (
            filteredEntries.map((entry, idx) => (
              <div key={idx} className={idx > 0 ? 'pt-4 space-y-2' : 'space-y-2'}>
                <div className="flex items-center justify-between flex-wrap gap-2">
                  <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                    {entry.term}
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-bold border border-slate-200">
                      {entry.category}
                    </span>
                  </h3>
                </div>

                <p className="text-xs text-slate-700 font-semibold bg-blue-50/60 p-2.5 rounded-xl border border-blue-100 leading-relaxed">
                  💡 <b>In Simple Words:</b> {entry.shortDef}
                </p>

                <p className="text-xs text-slate-600 leading-relaxed">
                  {entry.fullExplanation}
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 pt-1">
                  <div className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 text-[11px] space-y-1">
                    <span className="font-bold text-slate-700 block">🇮🇳 Indian Exporter Context</span>
                    <span className="text-slate-600">{entry.indianContext}</span>
                  </div>

                  <div className="p-2.5 rounded-xl bg-emerald-50/70 border border-emerald-200/80 text-[11px] space-y-1">
                    <span className="font-bold text-emerald-800 block">✅ Recommended Action</span>
                    <span className="text-emerald-900">{entry.actionableTip}</span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex items-center justify-between shrink-0">
          <span>Reviewed by Indian Export Domain & Legal Advisory • Version 2.0</span>
          <button
            type="button"
            onClick={() => setGlossaryModalOpen(false)}
            className="px-3 py-1 bg-slate-200 hover:bg-slate-300 rounded-lg text-slate-700 font-bold transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
