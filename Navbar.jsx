import React from 'react';
import { BarChart3, ShieldCheck, Sparkles, FolderUp, Activity, MessageSquare, Layers } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onExploreDemo, datasetName, isAskOpen, setIsAskOpen }) {
  return (
    <header className="sticky top-0 z-40 bg-[#080C14]/90 backdrop-blur-md border-b border-slate-800/80">
      <div className="prism-line w-full"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div 
          onClick={() => setActiveTab('landing')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-cyan-500 via-indigo-500 to-pink-500 p-[1px] flex items-center justify-center shadow-lg shadow-cyan-500/10 group-hover:shadow-cyan-500/20 transition-all">
            <div className="w-full h-full bg-[#0B111D] rounded-[7px] flex items-center justify-center">
              <span className="text-cyan-400 font-bold text-lg">P</span>
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg tracking-tight text-white font-heading">PRISM</span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                Decision AI
              </span>
            </div>
            <span className="text-[11px] text-slate-400 hidden sm:block">Pattern Reasoning & Insight System</span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center gap-1 bg-[#0F172A]/80 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              activeTab === 'overview'
                ? 'bg-slate-800 text-white shadow-sm border border-slate-700'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Activity className="w-4 h-4 text-cyan-400" />
            <span>Overview</span>
          </button>

          <button
            onClick={() => setActiveTab('insights')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              activeTab === 'insights'
                ? 'bg-slate-800 text-white shadow-sm border border-slate-700'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <BarChart3 className="w-4 h-4 text-violet-400" />
            <span>Insights</span>
          </button>

          <button
            onClick={() => setActiveTab('decisions')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              activeTab === 'decisions'
                ? 'bg-slate-800 text-white shadow-sm border border-slate-700'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Decision Center</span>
          </button>

          <button
            onClick={() => setActiveTab('upload')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
              activeTab === 'upload'
                ? 'bg-slate-800 text-white shadow-sm border border-slate-700'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <FolderUp className="w-4 h-4 text-pink-400" />
            <span>Upload</span>
          </button>
        </nav>

        {/* Quick Actions */}
        <div className="flex items-center gap-3">
          {datasetName && (
            <div className="hidden lg:flex items-center gap-2 text-xs bg-slate-900 border border-slate-800 px-2.5 py-1.5 rounded-lg text-slate-300">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="max-w-[140px] truncate">{datasetName}</span>
            </div>
          )}

          <button
            onClick={onExploreDemo}
            className="hidden sm:flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 hover:bg-cyan-500/20 transition-all"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Demo Data</span>
          </button>

          <button
            onClick={() => setIsAskOpen(!isAskOpen)}
            className={`flex items-center gap-2 text-xs font-semibold px-3 py-1.5 rounded-lg transition-all border ${
              isAskOpen
                ? 'bg-violet-600 text-white border-violet-500 shadow-lg shadow-violet-500/20'
                : 'bg-slate-900 text-slate-200 border-slate-800 hover:border-slate-700'
            }`}
          >
            <MessageSquare className="w-3.5 h-3.5 text-violet-400" />
            <span className="hidden sm:inline">Ask PRISM</span>
          </button>
        </div>

      </div>
    </header>
  );
}
