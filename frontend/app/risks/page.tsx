'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useProject } from '@/hooks/useProject';
import { fetchRisks } from '@/lib/api';
import { Risk } from '@/types';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingState } from '@/components/LoadingState';
import { ErrorState } from '@/components/ErrorState';
import { AlertOctagon, Sparkles, CheckCircle2, ShieldAlert, ArrowRight } from 'lucide-react';

export default function RisksPage() {
  const { selectedProjectId } = useProject();
  const [risks, setRisks] = useState<Risk[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadRisks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchRisks(selectedProjectId || undefined);
      setRisks(data);
    } catch (err: any) {
      console.error('Failed to load risks:', err);
      setError(err?.message || 'Failed to fetch risk intelligence telemetry');
    } finally {
      setIsLoading(false);
    }
  }, [selectedProjectId]);

  useEffect(() => {
    loadRisks();
  }, [loadRisks]);

  if (isLoading && risks.length === 0) {
    return <LoadingState message="Computing multi-factor EPC schedule & procurement risks..." />;
  }

  if (error && risks.length === 0) {
    return <ErrorState message={error} onRetry={loadRisks} />;
  }

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Schedule & Project Risk Intelligence' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <AlertOctagon className="h-6 w-6 text-rose-400" />
            Project Risk Matrix & AI Recovery Action Plans
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Dynamic risk scoring based on schedule slippage, submittal non-conformances, and supply chain bottlenecks.
          </p>
        </div>
      </div>

      {/* Risks Grid */}
      <div className="space-y-4">
        {risks.map((risk) => (
          <div
            key={risk.id}
            className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6 shadow-sm hover:border-slate-700 transition-colors space-y-5"
          >
            {/* Header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <StatusBadge status={risk.risk_level} />
                  <span className="rounded bg-slate-900 px-2 py-0.5 text-[10px] font-mono text-slate-400 border border-slate-800 uppercase">
                    Category: {risk.category}
                  </span>
                </div>
                <h3 className="text-base font-bold text-white mt-1">{risk.title}</h3>
              </div>

              <div className="flex items-center gap-4 bg-slate-900/80 p-3 rounded-xl border border-slate-800">
                <div className="text-right">
                  <p className="text-[10px] text-slate-500 uppercase font-mono">Risk Score</p>
                  <p className="text-lg font-bold font-mono text-rose-400">{risk.risk_score}/100</p>
                </div>
                <div className="h-6 w-px bg-slate-800" />
                <div className="text-right">
                  <p className="text-[10px] text-slate-500 uppercase font-mono">Schedule Impact</p>
                  <p className="text-lg font-bold font-mono text-orange-400">+{risk.impact_days} Days</p>
                </div>
              </div>
            </div>

            {/* Root Cause & Cascade */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-1">
                <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px]">
                  Root Cause
                </span>
                <p className="text-slate-200">{risk.root_cause}</p>
              </div>
              <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/40 space-y-1">
                <span className="font-semibold text-slate-400 uppercase tracking-wider text-[11px]">
                  Downstream Critical Cascade
                </span>
                <p className="text-slate-200">{risk.downstream_impact_summary}</p>
              </div>
            </div>

            {/* AI Mitigation Action Plans */}
            {risk.mitigations && risk.mitigations.length > 0 && (
              <div className="space-y-2 border-t border-slate-800/80 pt-4">
                <h4 className="text-xs font-semibold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles className="h-3.5 w-3.5" />
                  AI Recommended Recovery Action Plans ({risk.mitigations.length})
                </h4>
                <div className="space-y-2">
                  {risk.mitigations.map((mit) => (
                    <div
                      key={mit.id}
                      className="flex items-start justify-between gap-3 p-3 rounded-xl border border-cyan-900/30 bg-cyan-950/15 text-xs"
                    >
                      <div className="flex items-start gap-2.5">
                        <CheckCircle2 className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" />
                        <div>
                          <p className="font-medium text-slate-200">{mit.action_plan}</p>
                          <div className="flex items-center gap-3 text-[11px] text-slate-400 mt-1">
                            <span>Assignee: <strong className="text-slate-300">{mit.assigned_to || 'Unassigned'}</strong></span>
                            {mit.estimated_cost > 0 && <span>Est. Cost: <strong className="text-cyan-300 font-mono">${mit.estimated_cost.toLocaleString()}</strong></span>}
                          </div>
                        </div>
                      </div>
                      <StatusBadge status={mit.status} size="sm" />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
