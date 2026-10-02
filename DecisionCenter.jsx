import React, { useState } from 'react';
import { ShieldCheck, Target, Eye, FileText, CheckCircle2, AlertTriangle, ArrowRight, Filter } from 'lucide-react';

export default function DecisionCenter({ recommendations, onOpenEvidence }) {
  const [filterCategory, setFilterCategory] = useState('ALL');

  if (!recommendations) return null;

  const categories = ['ALL', 'HIGH PRIORITY', 'Sales Strategy', 'Inventory & Logistics', 'Data & Operations'];

  const filteredRecs = recommendations.filter(r => {
    if (filterCategory === 'ALL') return true;
    if (filterCategory === 'HIGH PRIORITY') return r.priority === 'HIGH';
    return r.dimension_category === filterCategory;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 mb-1">
            <ShieldCheck className="w-4 h-4" />
            <span>PRISM DECISION ENGINE</span>
          </div>
          <h2 className="text-2xl font-bold text-white font-heading">Decision Center</h2>
          <p className="text-sm text-slate-400">
            Actionable business recommendations grounded in detected dataset evidence.
          </p>
        </div>

        {/* Category Filter Tabs */}
        <div className="flex flex-wrap items-center gap-1 bg-[#0F172A] p-1 rounded-xl border border-slate-800 self-start sm:self-auto">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                filterCategory === cat
                  ? 'bg-emerald-500 text-black shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Decision Cards Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {filteredRecs.map((rec) => (
          <div key={rec.id} className="prism-card p-6 flex flex-col justify-between border-l-4 border-l-emerald-500">
            
            <div>
              {/* Header Badge */}
              <div className="flex items-center justify-between gap-2 mb-3">
                <div className="flex items-center gap-2">
                  <span className={`px-2.5 py-0.5 rounded text-[10px] font-extrabold uppercase ${
                    rec.priority === 'HIGH' ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                  }`}>
                    {rec.priority} PRIORITY
                  </span>
                  <span className="text-xs text-slate-400 font-mono">{rec.dimension_category}</span>
                </div>
                <span className="text-xs text-slate-500 font-mono">ID: {rec.id}</span>
              </div>

              {/* Title & Action */}
              <h3 className="text-lg font-bold text-white mb-3 font-heading">{rec.title}</h3>

              <div className="bg-[#0B111D] p-4 rounded-xl border border-slate-800/80 mb-4">
                <div className="text-xs font-bold uppercase text-emerald-400 mb-1 flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Recommended Business Action</span>
                </div>
                <p className="text-sm font-semibold text-white leading-relaxed">
                  {rec.action}
                </p>
              </div>

              {/* WHY Rationale */}
              <div className="mb-4 text-xs text-slate-300 space-y-1">
                <span className="font-semibold text-slate-400 block">Why this action?</span>
                <p className="text-slate-300 leading-relaxed bg-slate-900/40 p-2.5 rounded-lg border border-slate-800">
                  {rec.why}
                </p>
              </div>

              {/* Objective */}
              <div className="mb-4 text-xs">
                <span className="font-semibold text-slate-400 block mb-1">Expected Objective:</span>
                <div className="flex items-center gap-2 text-cyan-300 bg-cyan-500/10 p-2.5 rounded-lg border border-cyan-500/20">
                  <Target className="w-4 h-4 shrink-0" />
                  <span>{rec.expected_objective}</span>
                </div>
              </div>

              {/* Monitor Metrics */}
              <div className="mb-6">
                <span className="text-[11px] font-semibold text-slate-400 block mb-2">Metrics to Monitor Next:</span>
                <div className="flex flex-wrap gap-1.5">
                  {rec.monitor.map((m, idx) => (
                    <span key={idx} className="px-2.5 py-1 rounded bg-slate-800 text-slate-200 text-xs font-medium flex items-center gap-1">
                      <Eye className="w-3 h-3 text-slate-400" />
                      <span>{m}</span>
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Evidence Link Footer */}
            <div className="pt-4 border-t border-slate-800/80 flex items-center justify-between">
              <span className="text-xs text-emerald-400 font-semibold">{rec.confidence} CONFIDENCE</span>

              <button
                onClick={() => onOpenEvidence(rec.supporting_evidence_id)}
                className="px-3.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Inspect Evidence Trail</span>
              </button>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}
