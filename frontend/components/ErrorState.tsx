'use client';

import React from 'react';
import { AlertOctagon, RefreshCw } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Telemetry Connection Error',
  message = 'Failed to communicate with the backend API or retrieve database telemetry.',
  onRetry,
}) => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 rounded-xl border border-rose-900/40 bg-rose-950/20 min-h-[220px]">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-rose-900/40 border border-rose-800/60 text-rose-400 shadow-inner">
        <AlertOctagon className="h-6 w-6" />
      </div>
      <h4 className="mt-3 text-sm font-semibold text-rose-200">{title}</h4>
      <p className="mt-1 text-xs text-rose-300/80 max-w-md">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white text-xs font-medium shadow-md transition-all"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          <span>Retry Connection</span>
        </button>
      )}
    </div>
  );
};
