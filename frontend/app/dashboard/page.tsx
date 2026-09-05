'use client';

import React, { useEffect, useState, useCallback } from 'react';
import Link from 'next/link';
import { useProject } from '@/hooks/useProject';
import { fetchDashboardSummary, fetchProjects, triggerSeedDatabase } from '@/lib/api';
import { DashboardSummary } from '@/types';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { MetricCard } from '@/components/MetricCard';
import { HealthGaugeCard } from '@/components/HealthGaugeCard';
import { AlertBanner } from '@/components/AlertBanner';
import { LoadingState } from '@/components/LoadingState';
import { ErrorState } from '@/components/ErrorState';
import {
  Activity,
  AlertOctagon,
  Calendar,
  CheckCircle2,
  Cpu,
  FileText,
  ShieldCheck,
  Truck,
  Sparkles,
  ArrowUpRight,
  TrendingUp,
  Clock,
  DollarSign,
} from 'lucide-react';

export default function DashboardPage() {
  const { selectedProject, selectedProjectId, refreshProjects } = useProject();
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadSummary = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchDashboardSummary(selectedProjectId || undefined);
      setSummary(data);
    } catch (err: any) {
      console.error('Failed to load dashboard summary:', err);
      setError(err?.message || 'Failed to load project intelligence summary');
    } finally {
      setIsLoading(false);
    }
  }, [selectedProjectId]);

  useEffect(() => {
    loadSummary();
  }, [loadSummary]);

  if (isLoading && !summary) {
    return <LoadingState message="Loading Data Centre EPC telemetry..." />;
  }

  if (error && !summary) {
    return <ErrorState message={error} onRetry={loadSummary} />;
  }

  const health = summary?.project_health || {
    schedule: 65,
    procurement: 75,
    quality: 50,
    commissioning: 95,
  };

  const comp = summary?.compliance_summary || { total_checks: 4, passed: 2, failed: 1, warnings: 1 };
  const risks = summary?.risk_summary || { total_risks: 2, critical: 1, high: 1, medium: 0, low: 0 };
  const alerts = summary?.recent_alerts || [];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Breadcrumbs */}
      <Breadcrumbs items={[{ label: 'Executive Intelligence Dashboard' }]} />

      {/* Project Hero Header */}
      <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 p-6 shadow-xl">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className="rounded-md bg-cyan-500/10 px-2 py-0.5 text-xs font-mono font-bold text-cyan-400 border border-cyan-500/20">
                {summary?.project_code || 'TITAN-DC01'}
              </span>
              <span className="rounded-md bg-emerald-500/10 px-2 py-0.5 text-xs font-mono font-medium text-emerald-400 border border-emerald-500/20">
                Tier III 2N / N+1
              </span>
              <span className="rounded-md bg-slate-800 px-2 py-0.5 text-xs text-slate-400 font-mono">
                50MW Hyperscale
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
              {summary?.project_name || 'Project Titan DC-01 — 50MW Campus'}
            </h1>
            <p className="text-xs sm:text-sm text-slate-400 max-w-2xl">
              Turnkey engineering, procurement, construction, and integrated systems commissioning delivery.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800/80">
            <div className="space-y-1">
              <p className="text-[11px] text-slate-500 uppercase font-mono">Total Budget</p>
              <p className="text-base font-bold font-mono text-white">$345,000,000</p>
            </div>
            <div className="h-8 w-px bg-slate-800 hidden sm:block" />
            <div className="space-y-1">
              <p className="text-[11px] text-slate-500 uppercase font-mono">Target Handover</p>
              <p className="text-base font-bold font-mono text-cyan-400">240 Days</p>
            </div>
            <div className="h-8 w-px bg-slate-800 hidden sm:block" />
            <div className="space-y-1">
              <p className="text-[11px] text-slate-500 uppercase font-mono">Critical Path Float</p>
              <p className="text-base font-bold font-mono text-rose-400">-18 Days</p>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Health Gauges Grid */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Project Health & Delivery Telemetry
          </h2>
          <span className="text-[11px] text-slate-500 font-mono">Real-time dynamic scoring</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <HealthGaugeCard
            label="Schedule Health"
            score={health.schedule}
            category="schedule"
            subtitle="CPM Critical Path"
            statusText={health.schedule >= 80 ? 'ON SCHEDULE' : 'CRITICAL DELAY'}
          />
          <HealthGaugeCard
            label="Procurement Health"
            score={health.procurement}
            category="procurement"
            subtitle="Long-Lead Packages"
            statusText={health.procurement >= 80 ? 'ON TIME' : 'CUSTOMS HOLD'}
          />
          <HealthGaugeCard
            label="Quality & Spec Health"
            score={health.quality}
            category="quality"
            subtitle="Vendor Submittals"
            statusText={health.quality >= 80 ? 'COMPLIANT' : '1 NON-CONFORMANCE'}
          />
          <HealthGaugeCard
            label="Commissioning Health"
            score={health.commissioning}
            category="commissioning"
            subtitle="Levels 1-5 Readiness"
            statusText="IST PROTOCOL READY"
          />
        </div>
      </div>

      {/* Active AI Alerts Section */}
      {alerts.length > 0 && (
        <div className="space-y-2.5">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <AlertOctagon className="h-3.5 w-3.5 text-rose-400" />
              Active System & AI Alerts ({alerts.length})
            </h2>
            <span className="text-[11px] text-slate-500 font-mono">Prioritized action queue</span>
          </div>
          <div className="space-y-2">
            {alerts.map((alert, idx) => (
              <AlertBanner
                key={idx}
                title={alert.message}
                severity={alert.severity}
                actionHref={
                  alert.type === 'compliance_fail'
                    ? '/compliance'
                    : alert.type === 'schedule_risk'
                    ? '/risks'
                    : '/procurement'
                }
                actionText="Investigate Impact"
              />
            ))}
          </div>
        </div>
      )}

      {/* Quick Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Specification Deviations"
          value={`${comp.failed} Non-Compliant`}
          subtitle={`${comp.passed} verified PASS, ${comp.warnings} warnings`}
          icon={ShieldCheck}
          variant="rose"
          trend={{ value: 'Action Required', isPositive: false, label: 'UPS Efficiency -2.5%' }}
        />
        <MetricCard
          title="Schedule Critical Risks"
          value={`${risks.critical} Critical / ${risks.high} High`}
          subtitle="Transformer port customs clearance"
          icon={Calendar}
          variant="amber"
          trend={{ value: '+18 Days Delay', isPositive: false, label: 'Downstream impact' }}
        />
        <MetricCard
          title="Procurement Packages"
          value="5 Major Items"
          subtitle="1 package on customs hold"
          icon={Truck}
          variant="blue"
          trend={{ value: '$4.6M Total', isPositive: true, label: 'Committed spend' }}
        />
        <MetricCard
          title="Commissioning Tests"
          value="Level 1 to 5 IST"
          subtitle="FAT Passed, IST Pending"
          icon={CheckCircle2}
          variant="emerald"
          trend={{ value: '100% Prepared', isPositive: true, label: 'Test matrix' }}
        />
      </div>

      {/* Module Quick Navigators */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {/* Compliance Card */}
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-5 space-y-4 hover:border-slate-700 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">Spec Compliance</h3>
                <p className="text-xs text-slate-400">Automated submittal validation</p>
              </div>
            </div>
            <Link
              href="/compliance"
              className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <ArrowUpRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="space-y-2 text-xs border-t border-slate-800/80 pt-3">
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">UPS-01A Efficiency:</span>
              <span className="font-mono text-rose-400 font-bold">FAIL (94.0% vs 96.5%)</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">GEN-01A Start Time:</span>
              <span className="font-mono text-emerald-400">PASS (8.5s &le; 10s)</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">CH-01A Chiller COP:</span>
              <span className="font-mono text-emerald-400">PASS (6.45 &ge; 6.20)</span>
            </div>
          </div>
        </div>

        {/* Schedule CPM Card */}
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-5 space-y-4 hover:border-slate-700 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                <Calendar className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">Schedule CPM</h3>
                <p className="text-xs text-slate-400">Critical path dependencies</p>
              </div>
            </div>
            <Link
              href="/schedule"
              className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <ArrowUpRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="space-y-2 text-xs border-t border-slate-800/80 pt-3">
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">ACT-1020 MV Transformer:</span>
              <span className="font-mono text-orange-400">DELAYED (Customs hold)</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">ACT-1030 UPS Room Rigging:</span>
              <span className="font-mono text-cyan-400">45% In Progress</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">ACT-1050 MV Energization:</span>
              <span className="font-mono text-slate-400">Blocked by ACT-1020</span>
            </div>
          </div>
        </div>

        {/* Risk Mitigation Card */}
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-5 space-y-4 hover:border-slate-700 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-400">
                <AlertOctagon className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">Risk Intelligence</h3>
                <p className="text-xs text-slate-400">Calculated impact & mitigations</p>
              </div>
            </div>
            <Link
              href="/risks"
              className="p-1.5 rounded-lg border border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              <ArrowUpRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="space-y-2 text-xs border-t border-slate-800/80 pt-3">
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">Transformer Port Delay:</span>
              <span className="font-mono text-rose-400 font-bold">Score 88.5 (Critical)</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">UPS Efficiency Gap:</span>
              <span className="font-mono text-amber-400 font-bold">Score 72.0 (High)</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-500">Mitigation Status:</span>
              <span className="font-mono text-cyan-400">2 Action Plans Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
