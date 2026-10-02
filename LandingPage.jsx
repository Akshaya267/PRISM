import React from 'react';
import { ArrowRight, Sparkles, ShieldCheck, Cpu, LineChart, CheckCircle2, FileSearch, Layers } from 'lucide-react';

export default function LandingPage({ onAnalyzeClick, onExploreDemo }) {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex flex-col justify-between">
      {/* Hero Section */}
      <section className="relative pt-16 pb-20 overflow-hidden">
        {/* Background glow accents */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-gradient-to-r from-cyan-500/10 via-violet-500/10 to-pink-500/10 blur-[120px] rounded-full pointer-events-none"></div>

        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-300 text-xs font-semibold mb-8 backdrop-blur-md">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Evidence-Grounded AI Decision Intelligence</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-6 font-heading leading-tight">
            Turn Raw Business Data into <br />
            <span className="gradient-text-accent">Evidence-Based Decisions.</span>
          </h1>

          <p className="max-w-2xl mx-auto text-lg text-slate-300 mb-10 leading-relaxed">
            PRISM analyzes business data, uncovers meaningful patterns, traces insights back to mathematical evidence, and recommends actionable next steps.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <button
              onClick={onAnalyzeClick}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-semibold shadow-lg shadow-cyan-500/20 transition-all flex items-center justify-center gap-2 group cursor-pointer"
            >
              <span>Analyze Your Data</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>

            <button
              onClick={onExploreDemo}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 font-semibold border border-slate-700/80 transition-all flex items-center justify-center gap-2 cursor-pointer backdrop-blur-md"
            >
              <Sparkles className="w-4 h-4 text-cyan-400" />
              <span>Explore Demo Dataset</span>
            </button>
          </div>

          {/* PRISM Visual Workflow Metaphor */}
          <div className="w-full prism-card p-6 sm:p-8 relative overflow-hidden">
            <div className="text-xs uppercase tracking-widest text-slate-400 font-semibold mb-6">
              The PRISM Decision Flow
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 relative z-10">
              
              <div className="bg-[#0B111D] p-4 rounded-lg border border-slate-800 text-left">
                <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center mb-3 border border-blue-500/20">
                  <Layers className="w-4 h-4" />
                </div>
                <h3 className="font-semibold text-sm text-white mb-1">1. RAW DATA</h3>
                <p className="text-xs text-slate-400">CSV / XLSX Ingestion & Semantic Profiling</p>
              </div>

              <div className="bg-[#0B111D] p-4 rounded-lg border border-slate-800 text-left">
                <div className="w-8 h-8 rounded-lg bg-violet-500/10 text-violet-400 flex items-center justify-center mb-3 border border-violet-500/20">
                  <Cpu className="w-4 h-4" />
                </div>
                <h3 className="font-semibold text-sm text-white mb-1">2. INSIGHTS</h3>
                <p className="text-xs text-slate-400">Deterministic Trends & Contribution Analysis</p>
              </div>

              <div className="bg-[#0B111D] p-4 rounded-lg border border-slate-800 text-left">
                <div className="w-8 h-8 rounded-lg bg-pink-500/10 text-pink-400 flex items-center justify-center mb-3 border border-pink-500/20">
                  <FileSearch className="w-4 h-4" />
                </div>
                <h3 className="font-semibold text-sm text-white mb-1">3. EVIDENCE</h3>
                <p className="text-xs text-slate-400">Mathematical Calculation & Breakdown Trail</p>
              </div>

              <div className="bg-[#0B111D] p-4 rounded-lg border border-slate-800 text-left">
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-3 border border-emerald-500/20">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <h3 className="font-semibold text-sm text-white mb-1">4. ACTION</h3>
                <p className="text-xs text-slate-400">Evidence-Grounded Business Recommendations</p>
              </div>

            </div>
          </div>

        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="py-12 border-t border-slate-800/60 bg-[#060911]/60">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-6">
            
            <div className="prism-card p-6">
              <LineChart className="w-6 h-6 text-cyan-400 mb-4" />
              <h3 className="text-lg font-bold text-white mb-2">Zero AI Hallucinations</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Deterministic calculations handle numerical profiling, period comparisons, and contributions before natural language explanation.
              </p>
            </div>

            <div className="prism-card p-6">
              <FileSearch className="w-6 h-6 text-violet-400 mb-4" />
              <h3 className="text-lg font-bold text-white mb-2">Traceable Evidence Trails</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Every insight answers: What happened, why it happened, what formula supports it, and what segment contributed most.
              </p>
            </div>

            <div className="prism-card p-6">
              <CheckCircle2 className="w-6 h-6 text-emerald-400 mb-4" />
              <h3 className="text-lg font-bold text-white mb-2">Grounded Action Plans</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Recommends specific, data-backed operational next steps with rationale, expected outcome, and monitor metrics.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-6 border-t border-slate-900 text-center text-xs text-slate-500">
        <p>PRISM — Pattern Reasoning and Insight System for Management. Session data is private and processed locally.</p>
      </footer>
    </div>
  );
}
