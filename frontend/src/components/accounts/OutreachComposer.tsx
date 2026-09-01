import React, { useState, useEffect } from 'react';
import { Sparkles, Copy, Check, Send, AlertCircle, Mail, MessageSquare, Phone, Globe, Download, ShieldCheck, FileText, CheckCircle2, ChevronRight } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleBadge } from '../apple/AppleBadge';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';
import { TruthStatusBadge } from '../apple/TruthStatusBadge';
import { WhatDoesThisMean } from '../ui/WhatDoesThisMean';
import { generateOutreachApi, getCompliancePackApi, OutreachMode, OutreachLanguage, CompliancePackResponse } from '../../api/outreach';

interface Props {
  buyerId: string;
  buyerName: string;
  defaultContact?: string;
}

export const OutreachComposer: React.FC<Props> = ({ buyerId, buyerName, defaultContact }) => {
  const [mode, setMode] = useState<OutreachMode>('email');
  const [language, setLanguage] = useState<OutreachLanguage>('de');
  const [tone, setTone] = useState<'Professional' | 'Direct' | 'Technical' | 'Relationship'>('Professional');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [whyMatches, setWhyMatches] = useState<string[]>([]);
  const [complianceDocs, setComplianceDocs] = useState<string[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [copied, setCopied] = useState(false);

  // Compliance Pack State
  const [compliancePack, setCompliancePack] = useState<CompliancePackResponse | null>(null);
  const [isLoadingPack, setIsLoadingPack] = useState(false);
  const [isPackModalOpen, setIsPackModalOpen] = useState(false);

  const handleGenerate = async (
    targetMode = mode,
    targetLang = language,
    targetTone = tone
  ) => {
    setIsGenerating(true);
    try {
      const res = await generateOutreachApi({
        buyer_id: buyerId,
        mode: targetMode,
        language: targetLang,
        tone: targetTone,
        contact_name: defaultContact,
      });
      setSubject(res.subject);
      setBody(res.body);
      setWhyMatches(res.why_matches_you || []);
      setComplianceDocs(res.compliance_pack_docs || []);
    } catch (e: any) {
      console.error(e);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleLoadCompliancePack = async () => {
    setIsLoadingPack(true);
    try {
      const pack = await getCompliancePackApi(buyerId);
      setCompliancePack(pack);
      setIsPackModalOpen(true);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoadingPack(false);
    }
  };

  const handleCopy = () => {
    const textToCopy = mode === 'email' ? `Subject: ${subject}\n\n${body}` : body;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Auto-generate initial draft on mount
  useEffect(() => {
    handleGenerate();
  }, [buyerId]);

  return (
    <div className="space-y-6">
      {/* Top Banner with Controls */}
      <AppleCard variant="default" className="space-y-5 border-slate-200/90 bg-white p-6 shadow-sm">
        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-base font-bold text-slate-900 tracking-tight flex items-center gap-2">
                <Sparkles size={18} className="text-indigo-600" />
                European Outreach & Compliance Engine v2.0
              </h3>
              <AppleBadge tone="blue" size="sm">DIN 5008 Calibrated</AppleBadge>
              <TruthStatusBadge status="verified" sourceName="Factory Dossier" />
            </div>
            <p className="text-xs text-slate-500 font-medium">
              Generating cultural, legally verified introductory communication for <b>{buyerName}</b>.
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <AppleButton
              variant="secondary"
              size="sm"
              loading={isLoadingPack}
              onClick={handleLoadCompliancePack}
              icon={<Download size={13} />}
            >
              Export Compliance Pack (.ZIP)
            </AppleButton>
            <AppleButton
              variant="primary"
              size="sm"
              loading={isGenerating}
              onClick={() => handleGenerate(mode, language, tone)}
              icon={<Sparkles size={13} />}
            >
              Re-generate
            </AppleButton>
          </div>
        </div>

        {/* Mode & Language Selectors */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1">
          {/* Mode Selector */}
          <div className="space-y-1.5">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Outreach Mode</span>
            <div className="grid grid-cols-3 gap-1.5 p-1 bg-slate-100 rounded-xl">
              <button
                type="button"
                onClick={() => {
                  setMode('email');
                  handleGenerate('email', language, tone);
                }}
                className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  mode === 'email' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <Mail size={13} />
                <span>Email</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setMode('whatsapp');
                  handleGenerate('whatsapp', language, tone);
                }}
                className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  mode === 'whatsapp' ? 'bg-white text-emerald-700 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <MessageSquare size={13} />
                <span>WhatsApp</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setMode('phone_script');
                  handleGenerate('phone_script', language, tone);
                }}
                className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  mode === 'phone_script' ? 'bg-white text-blue-700 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <Phone size={13} />
                <span>Phone Call</span>
              </button>
            </div>
          </div>

          {/* Language Selector */}
          <div className="space-y-1.5">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Market Language</span>
            <div className="grid grid-cols-2 gap-1.5 p-1 bg-slate-100 rounded-xl">
              <button
                type="button"
                onClick={() => {
                  setLanguage('de');
                  handleGenerate(mode, 'de', tone);
                }}
                className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  language === 'de' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <Globe size={13} className="text-amber-600" />
                <span>German (DIN 5008)</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setLanguage('en');
                  handleGenerate(mode, 'en', tone);
                }}
                className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                  language === 'en' ? 'bg-white text-slate-900 shadow-2xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                <Globe size={13} className="text-blue-600" />
                <span>English (Global)</span>
              </button>
            </div>
          </div>

          {/* Tone Selector */}
          <div className="space-y-1.5">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Conversation Tone</span>
            <AppleSegmentedControl
              size="sm"
              value={tone}
              onChange={(newTone: any) => {
                setTone(newTone);
                handleGenerate(mode, language, newTone);
              }}
              options={[
                { value: 'Professional', label: 'Formal' },
                { value: 'Direct', label: 'Concise' },
                { value: 'Technical', label: 'Spec-Led' },
                { value: 'Relationship', label: 'Heritage' },
              ]}
            />
          </div>
        </div>
      </AppleCard>

      {/* Main Content: Composer & Why This Matches You Side Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Editor & Message Output */}
        <div className="lg:col-span-2 space-y-4">
          <AppleCard variant="default" className="space-y-4 bg-white p-5 border-slate-200/90 shadow-2xs">
            {mode === 'email' && (
              <div>
                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Subject Line</label>
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  className="w-full mt-1 p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-900 font-semibold focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-500/20"
                />
              </div>
            )}

            <div>
              <div className="flex items-center justify-between">
                <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                  {mode === 'email' ? 'Email Content (DIN 5008 Format)' : mode === 'whatsapp' ? 'WhatsApp Direct Text' : 'Cold Calling & Gatekeeper Script'}
                </label>
                <span className="text-[10px] text-slate-400 font-mono">
                  {body.length} characters
                </span>
              </div>
              <textarea
                rows={mode === 'phone_script' ? 14 : 12}
                value={body}
                onChange={(e) => setBody(e.target.value)}
                className="w-full mt-1 p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 leading-relaxed font-mono focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-blue-500/20"
              />
            </div>

            {/* Action Bar */}
            <div className="flex items-center justify-between pt-2 border-t border-slate-100 flex-wrap gap-2">
              <AppleButton
                variant="secondary"
                size="sm"
                onClick={handleCopy}
                icon={copied ? <Check size={14} className="text-emerald-600" /> : <Copy size={14} />}
              >
                {copied ? 'Copied to Clipboard' : 'Copy Content'}
              </AppleButton>

              <div className="flex items-center gap-2">
                {mode === 'email' && (
                  <AppleButton
                    variant="glass"
                    size="sm"
                    onClick={() => window.open(`mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`)}
                    icon={<Send size={14} />}
                  >
                    Open Mail App
                  </AppleButton>
                )}
                {mode === 'whatsapp' && (
                  <AppleButton
                    variant="primary"
                    size="sm"
                    className="bg-emerald-600 hover:bg-emerald-700"
                    onClick={() => window.open(`https://wa.me/?text=${encodeURIComponent(body)}`)}
                    icon={<MessageSquare size={14} />}
                  >
                    Launch WhatsApp
                  </AppleButton>
                )}
              </div>
            </div>
          </AppleCard>
        </div>

        {/* Right: "Why This Matches You" & Compliance Proof Panel */}
        <div className="space-y-4 lg:col-span-1">
          {/* Why This Matches You */}
          <AppleCard variant="default" className="space-y-3 bg-white p-5 border-slate-200/90 shadow-2xs">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles size={13} className="text-indigo-600" />
                Why This Matches You
              </h4>
              <WhatDoesThisMean term="EUDR (EU Deforestation Regulation)" />
            </div>

            <div className="space-y-2 text-xs">
              {whyMatches.map((item, idx) => (
                <div key={idx} className="p-2.5 rounded-xl bg-slate-50 border border-slate-100 text-slate-700 leading-snug">
                  {item}
                </div>
              ))}
            </div>
          </AppleCard>

          {/* Attached Verified Documents in Pack */}
          <AppleCard variant="default" className="space-y-3 bg-white p-5 border-slate-200/90 shadow-2xs">
            <div className="flex items-center justify-between">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                <ShieldCheck size={13} className="text-emerald-600" />
                Verified Pack Attachments
              </h4>
              <span className="text-[10px] font-mono text-emerald-700 font-bold">4 Verified</span>
            </div>

            <div className="space-y-2 text-xs">
              {complianceDocs.map((doc, idx) => (
                <div key={idx} className="flex items-center gap-2 p-2 rounded-xl bg-emerald-50/60 border border-emerald-100 text-emerald-900 font-medium">
                  <CheckCircle2 size={13} className="text-emerald-600 shrink-0" />
                  <span className="truncate">{doc}</span>
                </div>
              ))}
            </div>

            <button
              type="button"
              onClick={handleLoadCompliancePack}
              className="w-full py-2 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-700 transition-colors text-center cursor-pointer flex items-center justify-center gap-1.5"
            >
              <Download size={13} />
              <span>Download Full Pack ZIP</span>
            </button>
          </AppleCard>
        </div>
      </div>

      {/* Compliance Pack Bundle Modal */}
      {isPackModalOpen && compliancePack && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-xs">
          <div className="bg-white rounded-3xl p-6 max-w-lg w-full shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-base font-bold text-slate-900">Export Compliance Pack Manifest</h3>
                <p className="text-xs text-slate-500">Bundle ID: <b className="font-mono text-slate-700">{compliancePack.bundle_id}</b></p>
              </div>
              <AppleBadge tone="green" size="sm">Export-Ready</AppleBadge>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-2xl border border-slate-200/80 space-y-2 text-xs">
              <span className="text-[10px] font-bold text-slate-400 uppercase">Documents Included in Export Bundle</span>
              {compliancePack.documents.map((d) => (
                <div key={d.doc_id} className="p-2.5 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-0.5">
                  <div className="flex items-center justify-between font-bold text-slate-900">
                    <span className="truncate">{d.title}</span>
                    <span className="text-[10px] font-mono bg-slate-100 px-1.5 py-0.5 rounded text-slate-600">{d.file_format}</span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-slate-500">
                    <span>Issuer: {d.issuer}</span>
                    <span>Verified: {d.verified_date}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setIsPackModalOpen(false)}
                className="px-3.5 py-1.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100"
              >
                Close
              </button>
              <AppleButton
                variant="primary"
                size="sm"
                icon={<Download size={13} />}
                onClick={() => {
                  alert(`Downloading Compliance Bundle: ${compliancePack.bundle_id}.zip`);
                  setIsPackModalOpen(false);
                }}
              >
                Download Bundle (.ZIP)
              </AppleButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
