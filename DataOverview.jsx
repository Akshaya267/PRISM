import React from 'react';
import { Database, Calendar, AlertTriangle, CheckCircle2, DollarSign, Tag, Globe, Layers, ArrowRight } from 'lucide-react';

export default function DataOverview({ overview, onProceedToInsights }) {
  if (!overview) return null;

  const {
    dataset_name,
    total_rows,
    total_cols,
    date_range,
    missing_records_pct,
    duplicate_rows,
    column_profiles,
    detected_dimensions,
    key_metrics,
    quality_score,
    quality_warnings
  } = overview;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 prism-card p-6 border-l-4 border-l-cyan-500">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h2 className="text-2xl font-bold text-white font-heading">{dataset_name}</h2>
            <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Active Session
            </span>
          </div>
          <p className="text-sm text-slate-400">
            Dataset profiled & categorized into semantic business dimensions.
          </p>
        </div>

        <button
          onClick={onProceedToInsights}
          className="px-6 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-bold text-sm shadow-lg shadow-cyan-500/20 transition-all flex items-center justify-center gap-2 cursor-pointer self-start md:self-auto"
        >
          <span>View Insights & Evidence</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Grid Row 1: Summary Cards & Quality Gauge */}
      <div className="grid md:grid-cols-4 gap-6">
        
        <div className="prism-card p-5">
          <div className="text-xs text-slate-400 font-medium mb-1">Dataset Size</div>
          <div className="text-2xl font-bold text-white mb-2 font-heading">{total_rows.toLocaleString()} <span className="text-sm text-slate-400 font-normal">rows</span></div>
          <div className="text-xs text-slate-400">{total_cols} columns detected</div>
        </div>

        <div className="prism-card p-5">
          <div className="text-xs text-slate-400 font-medium mb-1">Date Time Span</div>
          <div className="text-sm font-bold text-cyan-300 mb-1">
            {date_range ? `${date_range.start} to ${date_range.end}` : "No temporal column"}
          </div>
          <div className="text-xs text-slate-400">Time-series auto-detected</div>
        </div>

        <div className="prism-card p-5">
          <div className="text-xs text-slate-400 font-medium mb-1">Data Completeness</div>
          <div className="text-2xl font-bold text-white mb-2 font-heading">{(100 - missing_records_pct).toFixed(1)}%</div>
          <div className="text-xs text-slate-400">{duplicate_rows} duplicate records</div>
        </div>

        <div className="prism-card p-5 flex items-center justify-between">
          <div>
            <div className="text-xs text-slate-400 font-medium mb-1">Data Health Score</div>
            <div className="text-3xl font-extrabold text-emerald-400 font-heading">{quality_score} <span className="text-sm font-normal text-slate-400">/ 100</span></div>
          </div>
          <div className="w-12 h-12 rounded-full border-4 border-emerald-500/30 border-t-emerald-400 flex items-center justify-center font-bold text-xs text-emerald-400">
            {quality_score >= 80 ? "EXC" : "GOOD"}
          </div>
        </div>

      </div>

      {/* Grid Row 2: Key Computed Business Metrics */}
      <div className="prism-card p-6">
        <h3 className="text-lg font-bold text-white mb-4 font-heading flex items-center gap-2">
          <DollarSign className="w-5 h-5 text-cyan-400" />
          <span>Automatically Identified Key Metrics</span>
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4">
          {Object.entries(key_metrics).map(([name, value]) => (
            <div key={name} className="bg-[#0B111D] p-4 rounded-lg border border-slate-800">
              <div className="text-xs text-slate-400 mb-1 truncate">{name}</div>
              <div className="text-lg font-bold text-white">
                {name.includes("Margin") ? `${value}%` : `$${value.toLocaleString()}`}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Grid Row 3: Detected Business Dimensions & Column Profiles */}
      <div className="grid md:grid-cols-3 gap-6">
        
        {/* Dimensions Mapping */}
        <div className="prism-card p-6 md:col-span-1">
          <h3 className="text-md font-bold text-white mb-4 font-heading flex items-center gap-2">
            <Layers className="w-4 h-4 text-violet-400" />
            <span>Semantic Role Detection</span>
          </h3>

          <div className="space-y-2.5">
            {Object.entries(detected_dimensions).map(([role, colName]) => (
              <div key={role} className="flex items-center justify-between text-xs py-1.5 border-b border-slate-800/60">
                <span className="capitalize text-slate-400 font-medium">{role}</span>
                <span className={`px-2 py-0.5 rounded font-mono font-semibold ${
                  colName ? 'bg-cyan-500/10 text-cyan-300 border border-cyan-500/20' : 'text-slate-600'
                }`}>
                  {colName || "Not present"}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Column Profiles Table */}
        <div className="prism-card p-6 md:col-span-2">
          <h3 className="text-md font-bold text-white mb-4 font-heading flex items-center gap-2">
            <Tag className="w-4 h-4 text-cyan-400" />
            <span>Detailed Column Schema</span>
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="pb-2 font-medium">Column Name</th>
                  <th className="pb-2 font-medium">Role</th>
                  <th className="pb-2 font-medium">Type</th>
                  <th className="pb-2 font-medium">Missing</th>
                  <th className="pb-2 font-medium">Sample Values</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {column_profiles.map((col) => (
                  <tr key={col.name} className="hover:bg-slate-800/30">
                    <td className="py-2.5 font-semibold text-white font-mono">{col.name}</td>
                    <td className="py-2.5">
                      <span className="px-2 py-0.5 rounded text-[11px] bg-slate-800 text-slate-300 font-medium">
                        {col.semantic_role}
                      </span>
                    </td>
                    <td className="py-2.5 text-slate-400">{col.data_type}</td>
                    <td className="py-2.5">
                      {col.missing_pct > 0 ? (
                        <span className="text-amber-400 font-semibold">{col.missing_pct}%</span>
                      ) : (
                        <span className="text-slate-500">0%</span>
                      )}
                    </td>
                    <td className="py-2.5 text-slate-400 font-mono truncate max-w-[150px]">
                      {col.sample_values.join(", ")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Quality Warnings */}
          {quality_warnings && quality_warnings.length > 0 && (
            <div className="mt-6 p-4 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300">
              <div className="font-semibold mb-1 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-amber-400" />
                <span>Data Quality Notes</span>
              </div>
              <ul className="list-disc list-inside space-y-1 text-slate-300">
                {quality_warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
