import React from 'react';
import { X, FileSearch, Calculator, Layers, CheckCircle2, AlertCircle, ShieldCheck, ArrowRight } from 'lucide-react';

export default function EvidenceModal({ evidence, onClose, onGoToAction }) {
  if (!evidence) return null;

  const {
    insight_id,
    claim,
    metric_name,
    calculation,
    top_contributors,
    supporting_factors,
    methods_used,
    confidence,
    analytical_reasoning
  } = evidence;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="glass-modal w-full max-w-3xl rounded-2xl p-6 sm:p-8 relative max-h-[90vh] overflow-y-auto border border-slate-700/80 shadow-2xl">
        
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-lg bg-slate-900 text-slate-400 hover:text-white transition-all cursor-pointer border border-slate-800"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-xs font-semibold text-cyan-400 mb-2">
            <FileSearch className="w-4 h-4" />
            <span>GROUNDED EVIDENCE TRAIL • {insight_id}</span>
          </div>
          <h2 className="text-2xl font-bold text-white font-heading">{claim}</h2>
        </div>

        {/* Audit Trail Steps */}
        <div className="space-y-6">
          
          {/* Step 1: Calculation Breakdown */}
          <div className="bg-[#0B111D] p-5 rounded-xl border border-slate-800">
            <div className="flex items-center gap-2 text-xs font-bold uppercase text-slate-400 mb-3">
              <Calculator className="w-4 h-4 text-cyan-400" />
              <span>1. Mathematical Calculation</span>
            </div>

            <div className="grid grid-cols-3 gap-4 text-center mb-4">
              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800">
                <div className="text-[11px] text-slate-400">Previous Period</div>
                <div className="text-base font-bold text-slate-200 font-mono">
                  ${calculation.previous_value.toLocaleString()}
                </div>
              </div>

              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800">
                <div className="text-[11px] text-slate-400">Current Period</div>
                <div className="text-base font-bold text-white font-mono">
                  ${calculation.current_value.toLocaleString()}
                </div>
              </div>

              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-800">
                <div className="text-[11px] text-slate-400">Variance Shift</div>
                <div className={`text-base font-bold font-mono ${
                  calculation.change_percent < 0 ? 'text-rose-400' : 'text-emerald-400'
                }`}>
                  {calculation.change_percent > 0 ? '+' : ''}{calculation.change_percent.toFixed(1)}%
                </div>
              </div>
            </div>

            <div className="text-xs font-mono text-cyan-300 bg-cyan-500/10 p-2.5 rounded-lg border border-cyan-500/20">
              Formula: {calculation.formula}
            </div>
          </div>

          {/* Step 2: Top Contributing Segments */}
          {top_contributors && top_contributors.length > 0 && (
            <div className="bg-[#0B111D] p-5 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2 text-xs font-bold uppercase text-slate-400 mb-3">
                <Layers className="w-4 h-4 text-violet-400" />
                <span>2. Contribution Waterfall Breakdown</span>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400">
                      <th className="pb-2">Dimension</th>
                      <th className="pb-2">Segment Value</th>
                      <th className="pb-2 text-right">Contribution %</th>
                      <th className="pb-2 text-right">Change Amount</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-mono">
                    {top_contributors.map((c, i) => (
                      <tr key={i}>
                        <td className="py-2 text-slate-400 capitalize">{c.dimension}</td>
                        <td className="py-2 font-bold text-white">{c.value}</td>
                        <td className="py-2 text-right text-cyan-400 font-bold">{c.contribution_percent}%</td>
                        <td className="py-2 text-right text-slate-300">${c.change_value.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Step 3: Supporting Factors */}
          {supporting_factors && supporting_factors.length > 0 && (
            <div className="bg-[#0B111D] p-5 rounded-xl border border-slate-800">
              <div className="flex items-center gap-2 text-xs font-bold uppercase text-slate-400 mb-3">
                <AlertCircle className="w-4 h-4 text-amber-400" />
                <span>3. Supporting Data Evidence</span>
              </div>

              <ul className="space-y-2 text-xs text-slate-300">
                {supporting_factors.map((f, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-1.5 shrink-0"></span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Step 4: Analytical Methods & Confidence */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
            <div>
              <span className="text-slate-400 block mb-1">Analytical Methodology Used:</span>
              <div className="flex flex-wrap gap-1.5">
                {methods_used.map((m, i) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                    {m}
                  </span>
                ))}
              </div>
            </div>

            <div className="text-right shrink-0">
              <span className="text-slate-400 block mb-1">Evidence Confidence:</span>
              <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/30">
                {confidence} CONFIDENCE
              </span>
            </div>
          </div>

        </div>

        {/* Action Button */}
        <div className="mt-8 pt-4 border-t border-slate-800 flex justify-end">
          <button
            onClick={onGoToAction}
            className="px-6 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-sm shadow-lg shadow-emerald-500/20 transition-all flex items-center gap-2 cursor-pointer"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>View Recommended Action</span>
          </button>
        </div>

      </div>
    </div>
  );
}
