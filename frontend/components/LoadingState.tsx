'use client';

import React from 'react';
import { Loader2 } from 'lucide-react';

export const LoadingState: React.FC<{ message?: string }> = ({ message = 'Loading intelligence telemetry...' }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[300px] p-8 text-center space-y-3">
      <div className="relative flex h-10 w-10 items-center justify-center">
        <div className="absolute h-10 w-10 rounded-full border-2 border-cyan-500/20 animate-ping" />
        <Loader2 className="h-6 w-6 text-cyan-400 animate-spin" />
      </div>
      <p className="text-xs font-medium text-slate-400 font-mono">{message}</p>
    </div>
  );
};

export const TableSkeleton: React.FC<{ rows?: number }> = ({ rows = 5 }) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4 space-y-3 animate-pulse">
      <div className="h-8 bg-slate-900 rounded-lg w-1/3 mb-4" />
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-10 bg-slate-900/60 rounded-lg w-full" />
      ))}
    </div>
  );
};
