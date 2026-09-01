'use client';

import React, { useState } from 'react';
import { Card } from '@/components/Card';
import { StatusBadge } from '@/components/StatusBadge';
import { useHealth } from '@/hooks/useHealth';
import { fetchPing } from '@/lib/api';
import {
  FileSearch,
  ShieldAlert,
  TrendingUp,
  Server,
  Zap,
  CheckCircle2,
  Database,
  Layers,
  Terminal,
  Activity,
} from 'lucide-react';

export default function DashboardLanding() {
  const { data: health, isLoading, error, latencyMs, lastChecked, refresh } = useHealth();
  const [pingResult, setPingResult] = useState<{ ping: string; time: string } | null>(null);
  const [isPinging, setIsPinging] = useState(false);

  const handleTestPing = async () => {
    setIsPinging(true);
    try {
      const res = await fetchPing();
      setPingResult(res);
    } catch (e: any) {
      setPingResult({ ping: `Error: ${e.message}`, time: new Date().toISOString() });
    } finally {
      setIsPinging(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold mb-3">
            <Zap className="w-3.5 h-3.5" />
            <span>Phase 1 Scaffolding Active</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white">
            Data Centre EPC Intelligence Platform
          </h1>
          <p className="mt-1 text-sm text-slate-400 max-w-2xl">
            Autonomous intelligence layer unifying specifications, vendor submittals, equipment procurement, and critical path risk analysis.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => refresh()}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-2"
          >
            <Activity className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh Health</span>
          </button>
          <button
            onClick={handleTestPing}
            disabled={isPinging}
            className="px-4 py-2 text-xs font-medium rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white shadow-lg shadow-cyan-600/20 transition flex items-center gap-2"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>{isPinging ? 'Testing Ping...' : 'Test Backend API'}</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="font-semibold uppercase tracking-wider">API Server</span>
              <StatusBadge
                status={error ? 'error' : health?.status === 'healthy' ? 'healthy' : 'degraded'}
                text={error ? 'Offline' : 'FastAPI v' + (health?.version || '0.1.0')}
              />
            </div>
            <p className="text-xl font-bold text-white">
              {health?.project ? 'FastAPI Online' : error ? 'Connection Error' : 'Connecting...'}
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
            <span>Latency:</span>
            <span className="font-mono text-cyan-400">{latencyMs !== null ? `${latencyMs}ms` : '--'}</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="font-semibold uppercase tracking-wider">Database</span>
              <Database className="w-4 h-4 text-slate-400" />
            </div>
            <p className="text-xl font-bold text-white">PostgreSQL + pgvector</p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
            <span>Status:</span>
            <span className="font-mono text-slate-200">
              {health?.services?.database?.status || 'Configured'}
            </span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="font-semibold uppercase tracking-wider">AI Engine</span>
              <Server className="w-4 h-4 text-slate-400" />
            </div>
            <p className="text-xl font-bold text-white capitalize">
              {health?.services?.llm_provider?.provider || 'Gemini 1.5 Pro'}
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
            <span>Embeddings:</span>
            <span className="font-mono text-slate-200">text-embedding-004</span>
          </div>
        </Card>

        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span className="font-semibold uppercase tracking-wider">Environment</span>
              <Layers className="w-4 h-4 text-slate-400" />
            </div>
            <p className="text-xl font-bold text-white capitalize">
              {health?.environment || 'Development'}
            </p>
          </div>
          <div className="mt-4 pt-3 border-t border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
            <span>Last Sync:</span>
            <span className="font-mono text-slate-200">
              {lastChecked ? lastChecked.toLocaleTimeString() : '--'}
            </span>
          </div>
        </Card>
      </div>

      {pingResult && (
        <div className="rounded-xl border border-cyan-500/30 bg-cyan-950/20 p-4 text-xs font-mono flex items-center justify-between">
          <div className="flex items-center gap-2 text-cyan-300">
            <CheckCircle2 className="w-4 h-4 text-cyan-400" />
            <span>FastAPI Live Response:</span>
            <span className="text-white font-bold">{JSON.stringify(pingResult)}</span>
          </div>
          <span className="text-slate-400 text-[11px]">{new Date(pingResult.time).toLocaleTimeString()}</span>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <h2 className="text-lg font-bold text-white">Core MVP Intelligence Modules</h2>
          <p className="text-xs text-slate-400">Three integrated AI systems scheduled for implementation.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card glow className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                <FileSearch className="w-6 h-6" />
              </div>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-cyan-400">
                Phase 4 & 5
              </span>
            </div>
            <div>
              <h3 className="font-bold text-base text-white">1. Project Knowledge Assistant</h3>
              <p className="mt-1.5 text-xs text-slate-400 leading-relaxed">
                RAG pipeline over EPC specifications, engineering drawings, standards, and vendor submittals with strict source citations and anti-hallucination verification.
              </p>
            </div>
          </Card>

          <Card glow className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                <ShieldAlert className="w-6 h-6" />
              </div>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-emerald-400">
                Phase 6
              </span>
            </div>
            <div>
              <h3 className="font-bold text-base text-white">2. Specification Compliance Agent</h3>
              <p className="mt-1.5 text-xs text-slate-400 leading-relaxed">
                Automated extraction and deterministic Python verification of technical parameters against vendor submittals.
              </p>
            </div>
          </Card>

          <Card glow className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400">
                <TrendingUp className="w-6 h-6" />
              </div>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-800 text-amber-400">
                Phase 7
              </span>
            </div>
            <div>
              <h3 className="font-bold text-base text-white">3. Schedule Risk Engine</h3>
              <p className="mt-1.5 text-xs text-slate-400 leading-relaxed">
                Critical path dependency graph mapping equipment procurement lead times, factory testing, site delivery, and commissioning.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
