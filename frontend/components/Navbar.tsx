'use client';

import React, { useState } from 'react';
import { StatusBadge } from './StatusBadge';
import { ProjectSelector } from './ProjectSelector';
import { useHealth } from '@/hooks/useHealth';
import { useProject } from '@/hooks/useProject';
import { triggerSeedDatabase } from '@/lib/api';
import { Database, Cpu, Activity, RefreshCw, Sparkles, Check } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { data, isLoading, error, latencyMs, refresh } = useHealth();
  const { refreshProjects } = useProject();
  const [isSeeding, setIsSeeding] = useState(false);
  const [seedSuccess, setSeedSuccess] = useState(false);

  const getStatus = (): 'healthy' | 'degraded' | 'error' | 'loading' => {
    if (isLoading && !data && !error) return 'loading';
    if (error) return 'error';
    if (data?.status === 'healthy') return 'healthy';
    return 'degraded';
  };

  const handleSeedData = async () => {
    try {
      setIsSeeding(true);
      await triggerSeedDatabase();
      await refreshProjects();
      await refresh();
      setSeedSuccess(true);
      setTimeout(() => setSeedSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to trigger seed data:', err);
    } finally {
      setIsSeeding(false);
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/90 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6">
        {/* Logo & Platform Info */}
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-tr from-cyan-600 to-blue-500 shadow-lg shadow-cyan-500/20 shrink-0">
            <Cpu className="h-5 w-5 text-white" />
          </div>
          <div className="hidden sm:block">
            <div className="flex items-center gap-2">
              <span className="font-bold text-sm tracking-tight text-white">
                DATA CENTRE EPC
              </span>
              <span className="rounded bg-cyan-500/10 px-1.5 py-0.2 text-[9px] font-semibold text-cyan-400 border border-cyan-500/20 font-mono">
                AI INTELLIGENCE
              </span>
            </div>
            <p className="text-[10px] text-slate-400">Mission-Critical Delivery Platform</p>
          </div>
        </div>

        {/* Center: Project Selector */}
        <div className="flex items-center gap-3">
          <ProjectSelector />
        </div>

        {/* Right: Telemetry & Actions */}
        <div className="flex items-center gap-3">
          <div className="hidden lg:flex items-center gap-3 text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <Database className="h-3.5 w-3.5 text-slate-400" />
              <span>DB:</span>
              <span className="text-slate-200 font-mono text-[11px]">
                {data?.services?.database?.status || 'checking...'}
              </span>
            </div>
            <span className="text-slate-700">|</span>
            <div className="flex items-center gap-1.5">
              <Activity className="h-3.5 w-3.5 text-slate-400" />
              <span>Latency:</span>
              <span className="text-slate-200 font-mono text-[11px]">
                {latencyMs !== null ? `${latencyMs}ms` : '--'}
              </span>
            </div>
          </div>

          <StatusBadge
            status={getStatus()}
            text={
              error
                ? 'Offline'
                : data?.status === 'healthy'
                ? 'Online'
                : 'Degraded'
            }
            size="sm"
          />

          {/* Quick Seed Button */}
          <button
            onClick={handleSeedData}
            disabled={isSeeding}
            title="Seed 50MW Data Centre Sample Data"
            className="hidden md:flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-slate-800 bg-slate-900/80 hover:bg-slate-800 text-xs font-medium text-slate-300 hover:text-white transition-all shadow-sm"
          >
            {seedSuccess ? (
              <>
                <Check className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-emerald-300">Seeded!</span>
              </>
            ) : (
              <>
                <Sparkles className={`h-3.5 w-3.5 text-cyan-400 ${isSeeding ? 'animate-spin' : ''}`} />
                <span>{isSeeding ? 'Seeding...' : 'Seed Data'}</span>
              </>
            )}
          </button>

          <button
            onClick={() => refresh()}
            title="Refresh Telemetry"
            className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>
    </header>
  );
};
