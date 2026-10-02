import React, { useState } from 'react';
import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { TrendingDown, TrendingUp, AlertTriangle, ShieldCheck, FileText, ArrowRight, Filter, ChevronRight } from 'lucide-react';

export default function InsightsDashboard({ insights, chartsData, onOpenEvidence, onViewRecommendation }) {
  const [filterImpact, setFilterImpact] = useState('ALL');

  if (!insights) return null;

  const filteredInsights = filterImpact === 'ALL'
    ? insights
    : insights.filter(i => i.impact === filterImpact);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white font-heading">Business Intelligence & Insights</h2>
          <p className="text-sm text-slate-400">
            Detected business trends, anomalies, and segment contributions grounded in evidence.
          </p>
        </div>

        {/* Impact Filter Tabs */}
        <div className="flex items-center gap-1 bg-[#0F172A] p-1 rounded-xl border border-slate-800 self-start sm:self-auto">
          {['ALL', 'HIGH', 'MEDIUM', 'LOW'].map((lvl) => (
            <button
              key={lvl}
              onClick={() => setFilterImpact(lvl)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                filterImpact === lvl
                  ? 'bg-cyan-500 text-black shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {lvl} {lvl !== 'ALL' && 'IMPACT'}
            </button>
          ))}
        </div>
      </div>

      {/* Interactive Charts Section */}
      {chartsData && (
        <div className="grid lg:grid-cols-3 gap-6">
          
          {/* Chart 1: Trend Over Time */}
          {chartsData.trend && (
            <div className="prism-card p-5 lg:col-span-2">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-md font-bold text-white font-heading">Revenue & Profit Trend</h3>
                  <p className="text-xs text-slate-400">Monthly aggregate performance</p>
                </div>
                <span className="text-[11px] font-semibold text-cyan-400 bg-cyan-500/10 px-2 py-0.5 rounded border border-cyan-500/20">
                  Time-Series
                </span>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={chartsData.trend}>
                    <defs>
                      <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.4}/>
                        <stop offset="95%" stopColor="#06B6D4" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorProf" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.4}/>
                        <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                    <XAxis dataKey="period" stroke="#64748B" fontSize={11} />
                    <YAxis stroke="#64748B" fontSize={11} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0B111D', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                      formatter={(val) => [`$${val.toLocaleString()}`, '']}
                    />
                    <Area type="monotone" dataKey="revenue" stroke="#06B6D4" fillOpacity={1} fill="url(#colorRev)" name="Revenue" />
                    <Area type="monotone" dataKey="profit" stroke="#8B5CF6" fillOpacity={1} fill="url(#colorProf)" name="Profit" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* Chart 2: Regional Performance */}
          {chartsData.region && (
            <div className="prism-card p-5 lg:col-span-1">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-md font-bold text-white font-heading">Regional Distribution</h3>
                  <p className="text-xs text-slate-400">Revenue split across regions</p>
                </div>
              </div>

              <div className="h-64 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartsData.region}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                    <XAxis dataKey="region" stroke="#64748B" fontSize={11} />
                    <YAxis stroke="#64748B" fontSize={11} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0B111D', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                      formatter={(val) => [`$${val.toLocaleString()}`, 'Revenue']}
                    />
                    <Bar dataKey="revenue" fill="#38BDF8" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

        </div>
      )}

      {/* Insight Feed */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white font-heading flex items-center gap-2">
          <span>Priority Insight Feed</span>
          <span className="text-xs font-normal text-slate-400">({filteredInsights.length} findings)</span>
        </h3>

        <div className="grid gap-4">
          {filteredInsights.map((ins) => {
            const isDecline = ins.change_pct < 0;
            const isHigh = ins.impact === 'HIGH';

            return (
              <div key={ins.id} className={`prism-card p-6 border-l-4 transition-all ${
                isHigh ? 'border-l-rose-500' : 'border-l-amber-500'
              }`}>
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                  
                  <div className="flex items-start gap-3">
                    <div className={`p-2 rounded-lg mt-0.5 ${
                      isDecline ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    }`}>
                      {isDecline ? <TrendingDown className="w-5 h-5" /> : <TrendingUp className="w-5 h-5" />}
                    </div>

                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider ${
                          isHigh ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        }`}>
                          {ins.impact} IMPACT
                        </span>
                        <span className="text-xs text-slate-500 font-mono">ID: {ins.id}</span>
                      </div>
                      <h4 className="text-lg font-bold text-white font-heading">{ins.title}</h4>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 self-end md:self-auto">
                    <button
                      onClick={() => onOpenEvidence(ins.id)}
                      className="px-3.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
                    >
                      <FileText className="w-3.5 h-3.5" />
                      <span>View Evidence</span>
                    </button>

                    <button
                      onClick={() => onViewRecommendation(ins.id)}
                      className="px-3.5 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer"
                    >
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>View Action</span>
                    </button>
                  </div>

                </div>

                <p className="text-sm text-slate-300 mb-4 leading-relaxed bg-[#0B111D] p-3 rounded-lg border border-slate-800/80">
                  {ins.what_happened}
                </p>

                {/* Evidence preview banner */}
                <div className="flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400 pt-2 border-t border-slate-800/60">
                  <div className="flex items-center gap-4">
                    <span>Metric: <strong className="text-white font-mono">{ins.metric_name}</strong></span>
                    <span>Variance: <strong className={`font-mono ${isDecline ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {ins.change_pct > 0 ? '+' : ''}{ins.change_pct.toFixed(1)}%
                    </strong></span>
                    <span>Segment: <strong className="text-slate-200">{ins.affected_segment}</strong></span>
                  </div>
                  <div className="text-cyan-400 font-medium flex items-center gap-1 cursor-pointer" onClick={() => onOpenEvidence(ins.id)}>
                    <span>Why am I seeing this?</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </div>
                </div>

              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
