'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useProject } from '@/hooks/useProject';
import { fetchComplianceResults, fetchSpecificationRequirements } from '@/lib/api';
import { ComplianceCheck, SpecificationRequirement } from '@/types';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { DataTable, Column } from '@/components/DataTable';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingState } from '@/components/LoadingState';
import { ErrorState } from '@/components/ErrorState';
import { ShieldCheck, AlertCircle, Sparkles, ChevronRight, CheckCircle2, HelpCircle } from 'lucide-react';

export default function CompliancePage() {
  const { selectedProjectId } = useProject();
  const [results, setResults] = useState<ComplianceCheck[]>([]);
  const [requirements, setRequirements] = useState<SpecificationRequirement[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCheck, setSelectedCheck] = useState<ComplianceCheck | null>(null);

  const loadData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const [checksData, reqsData] = await Promise.all([
        fetchComplianceResults(selectedProjectId || undefined),
        fetchSpecificationRequirements(selectedProjectId || undefined),
      ]);
      setResults(checksData);
      setRequirements(reqsData);
    } catch (err: any) {
      console.error('Failed to load compliance data:', err);
      setError(err?.message || 'Failed to fetch specification compliance telemetry');
    } finally {
      setIsLoading(false);
    }
  }, [selectedProjectId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const reqMap = React.useMemo(() => {
    const map = new Map<string, SpecificationRequirement>();
    requirements.forEach((r) => map.set(r.id, r));
    return map;
  }, [requirements]);

  const columns: Column<ComplianceCheck>[] = [
    {
      key: 'parameter',
      header: 'Parameter & Discipline',
      sortable: true,
      render: (check) => {
        const req = reqMap.get(check.requirement_id);
        return (
          <div>
            <span className="font-semibold text-slate-100 uppercase tracking-wide">
              {req?.parameter_name.replace(/_/g, ' ') || 'Requirement'}
            </span>
            <p className="text-[11px] text-slate-500 font-mono mt-0.5">
              {req?.section_reference || 'Spec Section'}
            </p>
          </div>
        );
      },
    },
    {
      key: 'required_value',
      header: 'Required Spec',
      render: (check) => {
        const req = reqMap.get(check.requirement_id);
        return (
          <span className="font-mono text-cyan-300 font-bold bg-cyan-950/40 px-2 py-1 rounded border border-cyan-800/40">
            {req?.operator} {req?.target_value_numeric} {req?.unit}
          </span>
        );
      },
    },
    {
      key: 'submitted_value',
      header: 'Vendor Submittal',
      render: (check) => (
        <span className="font-mono text-slate-200 font-bold bg-slate-900 px-2 py-1 rounded border border-slate-800">
          {check.submitted_value_numeric !== null ? `${check.submitted_value_numeric} ${check.submitted_unit || ''}` : check.submitted_value_text || 'N/A'}
        </span>
      ),
    },
    {
      key: 'deviation',
      header: 'Variance / Deviation',
      render: (check) => {
        if (check.deviation_numeric === null || check.deviation_numeric === undefined) return <span className="text-slate-500">None</span>;
        const isNegative = check.status === 'FAIL';
        return (
          <span className={`font-mono text-xs font-bold ${isNegative ? 'text-rose-400' : 'text-emerald-400'}`}>
            {check.deviation_numeric > 0 ? `+${check.deviation_numeric}` : check.deviation_numeric} {check.submitted_unit || ''}
          </span>
        );
      },
    },
    {
      key: 'severity',
      header: 'Severity',
      sortable: true,
      render: (check) => <StatusBadge status={check.severity} size="sm" />,
    },
    {
      key: 'status',
      header: 'Compliance Status',
      sortable: true,
      render: (check) => <StatusBadge status={check.status} />,
    },
    {
      key: 'details',
      header: 'AI Diagnostics',
      render: (check) => (
        <button
          onClick={() => setSelectedCheck(check)}
          className="flex items-center gap-1 px-2.5 py-1 rounded-lg border border-slate-800 bg-slate-900 hover:bg-slate-800 text-xs font-medium text-cyan-300 hover:text-cyan-200 transition-colors"
        >
          <Sparkles className="h-3.5 w-3.5 text-cyan-400" />
          <span>AI Breakdown</span>
        </button>
      ),
    },
  ];

  if (isLoading && results.length === 0) {
    return <LoadingState message="Running specification compliance matrix checks..." />;
  }

  if (error && results.length === 0) {
    return <ErrorState message={error} onRetry={loadData} />;
  }

  const passCount = results.filter((r) => r.status === 'PASS').length;
  const failCount = results.filter((r) => r.status === 'FAIL').length;
  const warnCount = results.filter((r) => r.status === 'WARNING').length;

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Specification Compliance & Submittal Verification' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <ShieldCheck className="h-6 w-6 text-cyan-400" />
            Specification Compliance Comparison Engine
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Automated comparison between contract specifications and vendor equipment submittals.
          </p>
        </div>

        {/* Quick summary badges */}
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono font-bold">
            {passCount} PASS
          </span>
          <span className="px-3 py-1 rounded-lg bg-rose-500/10 text-rose-400 border border-rose-500/20 text-xs font-mono font-bold">
            {failCount} FAIL
          </span>
          <span className="px-3 py-1 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20 text-xs font-mono font-bold">
            {warnCount} WARNING
          </span>
        </div>
      </div>

      <DataTable
        title="Specification Verification Records"
        subtitle="Automated parameter extraction & tolerance checks"
        columns={columns}
        data={results}
        filterTabs={[
          { label: 'All Checks', value: 'all', filterFn: () => true },
          { label: 'Failures Only', value: 'fail', filterFn: (r) => r.status === 'FAIL' },
          { label: 'Warnings', value: 'warn', filterFn: (r) => r.status === 'WARNING' },
          { label: 'Passed', value: 'pass', filterFn: (r) => r.status === 'PASS' },
        ]}
      />

      {/* AI Explanation Drawer Modal */}
      {selectedCheck && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-150">
          <div className="w-full max-w-2xl rounded-2xl border border-slate-800 bg-slate-950 p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                  <Sparkles className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">
                    AI Non-Conformance Diagnostic & Impact Analysis
                  </h3>
                  <p className="text-[11px] text-slate-400 font-mono">
                    Engineered Compliance Reasoning Engine v1
                  </p>
                </div>
              </div>
              <StatusBadge status={selectedCheck.status} />
            </div>

            <div className="space-y-4 text-xs">
              <div className="p-3.5 rounded-xl border border-slate-800 bg-slate-900/60 space-y-1">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  Deviation Summary
                </span>
                <p className="text-slate-200 font-medium">
                  {selectedCheck.deviation_description || 'No deviation details recorded.'}
                </p>
              </div>

              {selectedCheck.ai_explanation && (
                <div className="p-3.5 rounded-xl border border-cyan-900/40 bg-cyan-950/20 space-y-1">
                  <span className="text-[11px] font-semibold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                    <Sparkles className="h-3.5 w-3.5" />
                    Operational & Efficiency Impact Analysis
                  </span>
                  <p className="text-slate-300 leading-relaxed">
                    {selectedCheck.ai_explanation}
                  </p>
                </div>
              )}

              {selectedCheck.recommended_action && (
                <div className="p-3.5 rounded-xl border border-emerald-900/40 bg-emerald-950/20 space-y-1">
                  <span className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    Recommended Engineer Mitigation Action
                  </span>
                  <p className="text-emerald-200 font-medium leading-relaxed">
                    {selectedCheck.recommended_action}
                  </p>
                </div>
              )}
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedCheck(null)}
                className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-medium text-slate-200 transition-colors"
              >
                Close Diagnostic
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
