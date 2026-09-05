'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useProject } from '@/hooks/useProject';
import { fetchScheduleActivities } from '@/lib/api';
import { ScheduleActivity } from '@/types';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { DataTable, Column } from '@/components/DataTable';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingState } from '@/components/LoadingState';
import { ErrorState } from '@/components/ErrorState';
import { Calendar, AlertTriangle, Layers, Clock, CheckCircle2 } from 'lucide-react';

export default function SchedulePage() {
  const { selectedProjectId } = useProject();
  const [activities, setActivities] = useState<ScheduleActivity[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadActivities = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchScheduleActivities(selectedProjectId || undefined);
      setActivities(data);
    } catch (err: any) {
      console.error('Failed to load schedule activities:', err);
      setError(err?.message || 'Failed to fetch critical path schedule');
    } finally {
      setIsLoading(false);
    }
  }, [selectedProjectId]);

  useEffect(() => {
    loadActivities();
  }, [loadActivities]);

  const columns: Column<ScheduleActivity>[] = [
    {
      key: 'activity_code',
      header: 'Code',
      sortable: true,
      render: (act) => (
        <span className="font-mono text-cyan-400 font-bold bg-slate-900 px-2 py-1 rounded border border-slate-800">
          {act.activity_code}
        </span>
      ),
    },
    {
      key: 'name',
      header: 'Activity Name',
      sortable: true,
      render: (act) => (
        <div>
          <span className="font-semibold text-slate-100">{act.name}</span>
          <p className="text-[11px] text-slate-500 font-mono mt-0.5">WBS: {act.wbs || '1.0'}</p>
        </div>
      ),
    },
    {
      key: 'duration_days',
      header: 'Duration',
      render: (act) => <span className="font-mono text-slate-300">{act.duration_days} days</span>,
    },
    {
      key: 'percent_complete',
      header: 'Progress',
      render: (act) => (
        <div className="w-28 space-y-1">
          <div className="flex justify-between text-[10px] font-mono text-slate-400">
            <span>{act.percent_complete}%</span>
          </div>
          <div className="h-1.5 w-full bg-slate-900 rounded-full overflow-hidden border border-slate-800">
            <div
              className={`h-full rounded-full ${act.percent_complete === 100 ? 'bg-emerald-400' : 'bg-cyan-400'}`}
              style={{ width: `${act.percent_complete}%` }}
            />
          </div>
        </div>
      ),
    },
    {
      key: 'predecessors',
      header: 'Predecessors',
      render: (act) => (
        <div className="flex flex-wrap gap-1">
          {act.predecessors.length > 0 ? (
            act.predecessors.map((p) => (
              <span key={p} className="rounded bg-slate-900 px-1.5 py-0.2 text-[10px] font-mono text-slate-400 border border-slate-800">
                {p}
              </span>
            ))
          ) : (
            <span className="text-slate-600 text-[11px]">Start</span>
          )}
        </div>
      ),
    },
    {
      key: 'is_critical_path',
      header: 'Critical Path',
      sortable: true,
      render: (act) => (
        act.is_critical_path ? (
          <span className="rounded bg-rose-500/15 text-rose-400 border border-rose-500/30 px-2 py-0.5 text-[10px] font-mono font-bold uppercase">
            CRITICAL
          </span>
        ) : (
          <span className="rounded bg-slate-800 text-slate-400 px-2 py-0.5 text-[10px] font-mono">
            Float
          </span>
        )
      ),
    },
    {
      key: 'status',
      header: 'Execution Status',
      sortable: true,
      render: (act) => <StatusBadge status={act.status} />,
    },
  ];

  if (isLoading && activities.length === 0) {
    return <LoadingState message="Loading Critical Path Method (CPM) schedule..." />;
  }

  if (error && activities.length === 0) {
    return <ErrorState message={error} onRetry={loadActivities} />;
  }

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Schedule & Critical Path Method (CPM)' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <Calendar className="h-6 w-6 text-cyan-400" />
            Critical Path Method (CPM) Schedule
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Tracking milestone sequencing, predecessor networks, duration variances, and critical path risks.
          </p>
        </div>
      </div>

      <DataTable
        title="Schedule Activities & Milestones"
        subtitle="Primavera P6 / EPC Baseline Schedule"
        columns={columns}
        data={activities}
        searchKey={(a) => `${a.activity_code} ${a.name}`}
        filterTabs={[
          { label: 'All Activities', value: 'all', filterFn: () => true },
          { label: 'Critical Path Only', value: 'critical', filterFn: (a) => a.is_critical_path },
          { label: 'Delayed', value: 'delayed', filterFn: (a) => a.status === 'delayed' },
          { label: 'In Progress', value: 'prog', filterFn: (a) => a.status === 'in_progress' },
        ]}
      />
    </div>
  );
}
