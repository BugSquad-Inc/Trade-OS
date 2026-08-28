import React, { useState } from 'react';
import { Sparkles, Copy, Check, Send, AlertCircle } from 'lucide-react';
import { AppleCard } from '../apple/AppleCard';
import { AppleButton } from '../apple/AppleButton';
import { AppleSegmentedControl } from '../apple/AppleSegmentedControl';
import { generateOutreachApi } from '../../api/accounts';

interface Props {
  buyerId: string;
  buyerName: string;
  defaultContact?: string;
}

export const OutreachComposer: React.FC<Props> = ({ buyerId, buyerName, defaultContact }) => {
  const [tone, setTone] = useState<'Professional' | 'Direct' | 'Technical' | 'Relationship'>('Professional');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async (selectedTone = tone) => {
    setIsGenerating(true);
    try {
      const res = await generateOutreachApi({
        buyer_id: buyerId,
        tone: selectedTone,
        contact_name: defaultContact,
      });
      setSubject(res.subject);
      setBody(res.body);
    } catch (e: any) {
      console.error(e);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(`Subject: ${subject}

${body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <AppleCard variant="default" className="space-y-4 border-indigo-500/20 bg-white">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs">
            <Sparkles size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900 tracking-tight">AI Export Outreach Composer</h3>
            <p className="text-xs text-slate-500 font-medium">Personalized to {buyerName} with EUDR & Freight Context</p>
          </div>
        </div>

        <AppleButton
          variant="primary"
          size="sm"
          loading={isGenerating}
          onClick={() => handleGenerate()}
          icon={<Sparkles size={14} />}
        >
          Generate Message
        </AppleButton>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-500 font-bold uppercase tracking-wider">Outreach Tone:</span>
        <AppleSegmentedControl
          size="sm"
          value={tone}
          onChange={(newTone: any) => {
            setTone(newTone);
            handleGenerate(newTone);
          }}
          options={[
            { value: 'Professional', label: 'Professional' },
            { value: 'Direct', label: 'Direct & Concise' },
            { value: 'Technical', label: 'Technical Spec' },
            { value: 'Relationship', label: 'Relationship' },
          ]}
        />
      </div>

      <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/80 text-[11px] text-slate-600 flex items-center gap-2">
        <AlertCircle size={14} className="text-slate-400 shrink-0" />
        <span>Contact roles sourced from public directories under GDPR Art. 6(1)(f) Legitimate Interest — verify before outreach.</span>
      </div>

      {body ? (
        <div className="space-y-3 pt-2">
          <div>
            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Subject Line</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full mt-1 p-2.5 rounded-xl bg-white border border-slate-200 text-sm text-slate-900 font-semibold focus:outline-none focus:border-blue-500 shadow-2xs"
            />
          </div>

          <div>
            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Email Body</label>
            <textarea
              rows={10}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full mt-1 p-3 rounded-xl bg-white border border-slate-200 text-xs text-slate-800 leading-relaxed font-mono focus:outline-none focus:border-blue-500 shadow-2xs"
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <AppleButton
              variant="secondary"
              size="sm"
              onClick={handleCopy}
              icon={copied ? <Check size={14} className="text-emerald-600" /> : <Copy size={14} />}
            >
              {copied ? 'Copied to Clipboard' : 'Copy Message'}
            </AppleButton>

            <AppleButton
              variant="glass"
              size="sm"
              onClick={() => window.open(`mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`)}
              icon={<Send size={14} />}
            >
              Open in Mail App
            </AppleButton>
          </div>
        </div>
      ) : (
        <div className="p-8 text-center bg-slate-50 rounded-2xl border border-slate-200/80 text-xs text-slate-500 font-medium">
          Click <b className="text-slate-900 font-bold">"Generate Message"</b> to draft a personalized outreach email for {buyerName}.
        </div>
      )}
    </AppleCard>
  );
};
