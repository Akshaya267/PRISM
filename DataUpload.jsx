import React, { useState } from 'react';
import { Upload, FileSpreadsheet, Sparkles, CheckCircle2, AlertTriangle, ArrowRight, Loader2, Info } from 'lucide-react';

export default function DataUpload({ onFileUpload, onExploreDemo, isLoading, loadingStep }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      onFileUpload(file);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      onFileUpload(file);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold text-white mb-3 font-heading">
          Upload Your Business Dataset
        </h2>
        <p className="text-slate-400 text-sm max-w-xl mx-auto">
          PRISM accepts CSV or Excel business files. The system automatically inspects columns, cleans dirty values, detects metrics, and builds evidence trails.
        </p>
      </div>

      {isLoading ? (
        <div className="prism-card p-12 text-center flex flex-col items-center justify-center min-h-[340px]">
          <div className="w-16 h-16 rounded-full bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center mb-6">
            <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
          </div>
          <h3 className="text-xl font-bold text-white mb-2">Analyzing Business Dataset...</h3>
          <p className="text-sm text-cyan-400 font-mono transition-all animate-pulse">
            {loadingStep || "Profiling data & generating evidence trails..."}
          </p>
          
          {/* Progress sequence bar */}
          <div className="w-full max-w-md bg-slate-900 h-2 rounded-full mt-8 overflow-hidden border border-slate-800">
            <div className="h-full bg-gradient-to-r from-cyan-500 via-indigo-500 to-pink-500 animate-pulse w-3/4"></div>
          </div>
        </div>
      ) : (
        <div className="grid gap-8">
          
          {/* Drag and Drop Zone */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`prism-card p-10 text-center border-2 border-dashed transition-all relative cursor-pointer ${
              dragActive 
                ? 'border-cyan-400 bg-cyan-500/5' 
                : 'border-slate-800 hover:border-slate-700'
            }`}
          >
            <input
              type="file"
              accept=".csv, .xlsx, .xls"
              onChange={handleFileChange}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />

            <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 flex items-center justify-center mx-auto mb-4">
              <Upload className="w-8 h-8" />
            </div>

            <h3 className="text-lg font-semibold text-white mb-1">
              Drag & Drop your CSV or Excel file here
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Supported formats: .csv, .xlsx, .xls (up to 50MB)
            </p>

            <div className="inline-flex items-center gap-3">
              <label className="px-5 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-black font-semibold text-sm cursor-pointer shadow-lg shadow-cyan-500/10 transition-all">
                Browse Files
              </label>

              <span className="text-xs text-slate-500">or</span>

              <button
                type="button"
                onClick={onExploreDemo}
                className="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 font-semibold text-sm border border-slate-700 transition-all flex items-center gap-2 cursor-pointer"
              >
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <span>Use Demo Dataset</span>
              </button>
            </div>
          </div>

          {/* Privacy Note */}
          <div className="flex items-center justify-center gap-2 text-xs text-slate-500 bg-slate-900/40 p-3 rounded-lg border border-slate-800/60">
            <Info className="w-4 h-4 text-cyan-400" />
            <span>Privacy Note: Your uploaded dataset is processed locally and used only for this analysis session.</span>
          </div>

        </div>
      )}
    </div>
  );
}
