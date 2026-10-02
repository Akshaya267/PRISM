import React, { useState } from 'react';
import { X, Send, Sparkles, MessageSquare, ShieldCheck, AlertCircle, FileText, Loader2 } from 'lucide-react';

export default function AskPrism({ isOpen, onClose, onOpenEvidence }) {
  const [question, setQuestion] = useState('');
  const [chatLog, setChatLog] = useState([
    {
      sender: 'prism',
      text: 'Hello! I am PRISM AI. Ask me questions about your uploaded dataset. I will answer strictly using deterministic calculations and evidence.',
      facts: [],
      evidenceId: null
    }
  ]);
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const sampleQuestions = [
    "Why did revenue decline?",
    "Which region performed worst?",
    "Which product contributed most?",
    "What should we investigate first?"
  ];

  const handleSend = async (qText) => {
    const userQuery = qText || question;
    if (!userQuery.trim() || loading) return;

    // Append User Message
    setChatLog(prev => [...prev, { sender: 'user', text: userQuery }]);
    setQuestion('');
    setLoading(true);

    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userQuery })
      });

      if (res.ok) {
        const data = await res.json();
        setChatLog(prev => [
          ...prev,
          {
            sender: 'prism',
            text: data.answer,
            facts: data.grounded_facts || [],
            evidenceId: data.supporting_evidence_id,
            dataFound: data.data_found
          }
        ]);
      } else {
        setChatLog(prev => [
          ...prev,
          {
            sender: 'prism',
            text: 'An error occurred while querying the analytical engine.',
            facts: []
          }
        ]);
      }
    } catch (e) {
      setChatLog(prev => [
        ...prev,
        {
          sender: 'prism',
          text: 'Could not connect to PRISM backend query server.',
          facts: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full sm:w-96 glass-modal border-l border-slate-700 shadow-2xl flex flex-col justify-between">
      
      {/* Header */}
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-violet-500/20 text-violet-400 border border-violet-500/30 flex items-center justify-center">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-sm text-white font-heading">Ask PRISM AI</h3>
            <span className="text-[10px] text-cyan-400">Zero-Hallucination Query Engine</span>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white transition-all cursor-pointer border border-slate-800"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Chat History Container */}
      <div className="p-4 flex-1 overflow-y-auto space-y-4 text-xs">
        {chatLog.map((msg, idx) => (
          <div
            key={idx}
            className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            <div className={`p-3 rounded-xl max-w-[88%] leading-relaxed ${
              msg.sender === 'user'
                ? 'bg-cyan-500 text-black font-medium rounded-br-none'
                : 'bg-[#0B111D] border border-slate-800 text-slate-200 rounded-bl-none'
            }`}>
              {msg.text}
            </div>

            {/* Grounded Facts Sub-box */}
            {msg.facts && msg.facts.length > 0 && (
              <div className="mt-2 p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 text-[11px] text-slate-300 max-w-[88%] space-y-1">
                <span className="font-semibold text-cyan-400 block mb-1">Grounded Data Facts:</span>
                {msg.facts.map((f, i) => (
                  <div key={i} className="flex items-start gap-1.5">
                    <span className="text-cyan-400 font-mono">•</span>
                    <span>{f}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Evidence Link Button */}
            {msg.evidenceId && (
              <button
                onClick={() => onOpenEvidence(msg.evidenceId)}
                className="mt-2 px-2.5 py-1 rounded bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-slate-700 text-[10px] font-semibold flex items-center gap-1 transition-all cursor-pointer"
              >
                <FileText className="w-3 h-3" />
                <span>Inspect Evidence Trail ({msg.evidenceId})</span>
              </button>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-2 text-xs text-cyan-400">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>Calculating data query facts...</span>
          </div>
        )}
      </div>

      {/* Sample Question Chips */}
      <div className="px-4 py-2 border-t border-slate-800/80 bg-[#060911]/60">
        <div className="text-[10px] text-slate-500 font-semibold mb-1.5 uppercase">Suggested Questions:</div>
        <div className="flex flex-wrap gap-1">
          {sampleQuestions.map((sq, i) => (
            <button
              key={i}
              onClick={() => handleSend(sq)}
              className="text-[11px] px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 cursor-pointer transition-all"
            >
              {sq}
            </button>
          ))}
        </div>
      </div>

      {/* Input Box */}
      <div className="p-3 border-t border-slate-800 bg-[#0B111D]">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask PRISM about your data..."
            className="flex-1 bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
          <button
            onClick={() => handleSend()}
            disabled={loading || !question.trim()}
            className="p-2 rounded-lg bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-black font-bold cursor-pointer transition-all shrink-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

    </div>
  );
}
