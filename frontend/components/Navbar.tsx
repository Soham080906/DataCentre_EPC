'use client';

import React from 'react';
import { StatusBadge } from './StatusBadge';
import { useHealth } from '@/hooks/useHealth';
import { Database, Cpu, Activity, RefreshCw } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { data, isLoading, error, latencyMs, refresh } = useHealth();

  const getStatus = (): 'healthy' | 'degraded' | 'error' | 'loading' => {
    if (isLoading && !data && !error) return 'loading';
    if (error) return 'error';
    if (data?.status === 'healthy') return 'healthy';
    return 'degraded';
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-tr from-cyan-600 to-blue-500 shadow-lg shadow-cyan-500/20">
            <Cpu className="h-6 w-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base tracking-tight text-white">
                DATA CENTRE EPC
              </span>
              <span className="rounded bg-cyan-500/10 px-1.5 py-0.5 text-[10px] font-semibold text-cyan-400 border border-cyan-500/20">
                AI INTELLIGENCE
              </span>
            </div>
            <p className="text-xs text-slate-400">Engineering • Procurement • Construction Analytics</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden md:flex items-center gap-3 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <Database className="h-3.5 w-3.5 text-slate-400" />
              <span>DB:</span>
              <span className="text-slate-200 font-mono">
                {data?.services?.database?.status || 'checking...'}
              </span>
            </div>
            <span className="text-slate-700">|</span>
            <div className="flex items-center gap-1.5">
              <Activity className="h-3.5 w-3.5 text-slate-400" />
              <span>Latency:</span>
              <span className="text-slate-200 font-mono">
                {latencyMs !== null ? `${latencyMs}ms` : '--'}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <StatusBadge
              status={getStatus()}
              text={
                error
                  ? 'API Offline'
                  : data?.status === 'healthy'
                  ? 'FastAPI Connected'
                  : 'Degraded'
              }
            />
            <button
              onClick={() => refresh()}
              title="Refresh System Health"
              className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
