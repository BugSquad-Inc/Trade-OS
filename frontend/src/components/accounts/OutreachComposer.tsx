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
    <AppleCard variant="default" className="space-y-4 border-indigo-500/20">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Sparkles size={18} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">AI Export Outreach Composer</h3>
            <p className="text-xs text-zinc-400">Personalized to {buyerName} with EUDR & Freight Context</p>
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
        <span className="text-zinc-400 font-semibold uppercase tracking-wider">Outreach Tone:</span>
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

      <div className="p-2.5 bg-zinc-950/60 rounded-xl border border-white/[0.06] text-[11px] text-zinc-400 flex items-center gap-2">
        <AlertCircle size={14} className="text-zinc-500 shrink-0" />
        <span>Contact roles sourced from public directories under GDPR Art. 6(1)(f) Legitimate Interest — verify before outreach.</span>
      </div>

      {body ? (
        <div className="space-y-3 pt-2">
          <div>
            <label className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">Subject Line</label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full mt-1 p-2.5 rounded-xl bg-zinc-950/80 border border-white/[0.08] text-sm text-white font-medium focus:outline-none focus:border-blue-500/50"
            />
          </div>

          <div>
            <label className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider">Email Body</label>
            <textarea
              rows={10}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full mt-1 p-3 rounded-xl bg-zinc-950/80 border border-white/[0.08] text-xs text-zinc-200 leading-relaxed font-sans focus:outline-none focus:border-blue-500/50 font-mono"
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <AppleButton
              variant="secondary"
              size="sm"
              onClick={handleCopy}
              icon={copied ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
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
        <div className="p-8 text-center bg-zinc-950/40 rounded-xl border border-white/[0.05] text-xs text-zinc-400">
          Click <b className="text-white">"Generate Message"</b> to draft a personalized outreach email for {buyerName}.
        </div>
      )}
    </AppleCard>
  );
};
