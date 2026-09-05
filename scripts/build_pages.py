import os

pages = {}

# Layout
pages['frontend/app/layout.tsx'] = r"""import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';
import { Sidebar } from '@/components/Sidebar';
import { ProjectProvider } from '@/hooks/useProject';

export const metadata: Metadata = {
  title: 'Data Centre EPC | AI Intelligence Platform',
  description: 'AI intelligence layer over Data Centre Engineering, Procurement, Construction, and Commissioning Delivery.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased font-sans flex flex-col selection:bg-cyan-500/30 selection:text-cyan-200">
        <ProjectProvider>
          <Navbar />
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
              <div className="max-w-7xl mx-auto space-y-6">
                {children}
              </div>
            </main>
          </div>
        </ProjectProvider>
      </body>
    </html>
  );
}
"""

# Dashboard Page (both /dashboard and /)
dashboard_page = r"""'use client';

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
"""

pages['frontend/app/page.tsx'] = dashboard_page
pages['frontend/app/dashboard/page.tsx'] = dashboard_page

# Documents Page
pages['frontend/app/documents/page.tsx'] = """'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useProject } from '@/hooks/useProject';
import { fetchDocuments, fetchDocumentChunks } from '@/lib/api';
import { Document, DocumentChunk } from '@/types';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { DataTable, Column } from '@/components/DataTable';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingState } from '@/components/LoadingState';
import { ErrorState } from '@/components/ErrorState';
import { FileText, Eye, Layers, FileCode, CheckCircle, Clock } from 'lucide-react';

export default function DocumentsPage() {
  const { selectedProjectId } = useProject();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [chunks, setChunks] = useState<DocumentChunk[]>([]);
  const [loadingChunks, setLoadingChunks] = useState<boolean>(false);

  const loadDocuments = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchDocuments(selectedProjectId || undefined);
      setDocuments(data);
    } catch (err: any) {
      console.error('Failed to load documents:', err);
      setError(err?.message || 'Failed to fetch project documents');
    } finally {
      setIsLoading(false);
    }
  }, [selectedProjectId]);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const handleInspectChunks = async (doc: Document) => {
    setSelectedDoc(doc);
    try {
      setLoadingChunks(true);
      const data = await fetchDocumentChunks(doc.id);
      setChunks(data);
    } catch (err) {
      console.error('Failed to load chunks:', err);
    } finally {
      setLoadingChunks(false);
    }
  };

  const columns: Column<Document>[] = [
    {
      key: 'filename',
      header: 'Document Name',
      sortable: true,
      render: (doc) => (
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-cyan-400">
            <FileText className="h-4 w-4" />
          </div>
          <div>
            <span className="font-semibold text-slate-100">{doc.filename}</span>
            <p className="text-[11px] text-slate-500 font-mono mt-0.5">{doc.file_path}</p>
          </div>
        </div>
      ),
    },
    {
      key: 'file_type',
      header: 'Category',
      sortable: true,
      render: (doc) => (
        <span className="rounded bg-slate-900 px-2 py-0.5 font-mono text-[11px] text-slate-300 border border-slate-800 uppercase">
          {doc.file_type.replace('_', ' ')}
        </span>
      ),
    },
    {
      key: 'version',
      header: 'Version',
      render: (doc) => <span className="font-mono text-slate-300">v{doc.version}</span>,
    },
    {
      key: 'total_pages',
      header: 'Pages',
      render: (doc) => <span className="font-mono text-slate-300">{doc.total_pages} pgs</span>,
    },
    {
      key: 'file_size',
      header: 'Size',
      render: (doc) => (
        <span className="font-mono text-slate-400">
          {(doc.file_size / (1024 * 1024)).toFixed(2)} MB
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Index Status',
      sortable: true,
      render: (doc) => <StatusBadge status={doc.status} />,
    },
    {
      key: 'actions',
      header: 'Inspection',
      render: (doc) => (
        <button
          onClick={() => handleInspectChunks(doc)}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-slate-800 bg-slate-900 hover:bg-slate-800 text-xs font-medium text-cyan-300 hover:text-cyan-200 transition-colors"
        >
          <Layers className="h-3.5 w-3.5 text-cyan-400" />
          <span>View Chunks</span>
        </button>
      ),
    },
  ];

  if (isLoading && documents.length === 0) {
    return <LoadingState message="Loading engineering specification documents..." />;
  }

  if (error && documents.length === 0) {
    return <ErrorState message={error} onRetry={loadDocuments} />;
  }

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Engineering Documents & Specifications' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
            Document Repository & Specification Ingestion
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Centrally indexed engineering specifications, drawings, vendor submittals, and test procedures with pgvector embeddings.
          </p>
        </div>
      </div>

      <DataTable
        title="Indexed Project Documents"
        subtitle="Searchable specifications and vendor submittals"
        columns={columns}
        data={documents}
        searchKey={(doc) => `${doc.filename} ${doc.file_type}`}
        filterTabs={[
          { label: 'All Documents', value: 'all', filterFn: () => true },
          { label: 'Specifications', value: 'spec', filterFn: (d) => d.file_type === 'specification' },
          { label: 'Vendor Submittals', value: 'sub', filterFn: (d) => d.file_type === 'vendor_submittal' },
        ]}
      />

      {/* Chunks Inspection Modal / Drawer */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-150">
          <div className="w-full max-w-3xl max-h-[85vh] overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 p-6 shadow-2xl flex flex-col space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <FileCode className="h-4 w-4 text-cyan-400" />
                  {selectedDoc.filename}
                </h3>
                <p className="text-xs text-slate-400 font-mono mt-0.5">
                  Extracted 768-dim Embeddings & Paragraph Chunks
                </p>
              </div>
              <button
                onClick={() => setSelectedDoc(null)}
                className="px-3 py-1 rounded-lg border border-slate-800 text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-900"
              >
                Close
              </button>
            </div>

            <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar pr-2">
              {loadingChunks ? (
                <LoadingState message="Retrieving text chunks..." />
              ) : chunks.length > 0 ? (
                chunks.map((chunk) => (
                  <div key={chunk.id} className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-2">
                    <div className="flex items-center justify-between text-xs font-mono text-cyan-400">
                      <span>Chunk #{chunk.chunk_index} {chunk.page_number ? `(Page ${chunk.page_number})` : ''}</span>
                      <span className="text-slate-500 font-sans">{chunk.token_count} tokens</span>
                    </div>
                    {chunk.section_header && (
                      <p className="text-xs font-bold text-slate-200 uppercase tracking-wide">
                        {chunk.section_header}
                      </p>
                    )}
                    <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3 rounded-lg border border-slate-800/60 font-mono">
                      {chunk.content}
                    </p>
                  </div>
                ))
              ) : (
                <div className="p-8 text-center text-xs text-slate-500">
                  No text chunks extracted yet for this document.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""

pages['frontend/app/compliance/page.tsx'] = r"""'use client';

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
"""

# Schedule Page
pages['frontend/app/schedule/page.tsx'] = """'use client';

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
"""

# Procurement Page
pages['frontend/app/procurement/page.tsx'] = """'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useProject } from '@/hooks/useProject';
import { fetchProcurementItems } from '@/lib/api';
import { ProcurementItem } from '@/types';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { DataTable, Column } from '@/components/DataTable';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingState } from '@/components/LoadingState';
import { ErrorState } from '@/components/ErrorState';
import { Truck, AlertTriangle, ShieldAlert, DollarSign } from 'lucide-react';

export default function ProcurementPage() {
  const { selectedProjectId } = useProject();
  const [items, setItems] = useState<ProcurementItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadItems = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchProcurementItems(selectedProjectId || undefined);
      setItems(data);
    } catch (err: any) {
      console.error('Failed to load procurement items:', err);
      setError(err?.message || 'Failed to fetch equipment procurement records');
    } finally {
      setIsLoading(false);
    }
  }, [selectedProjectId]);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const columns: Column<ProcurementItem>[] = [
    {
      key: 'item_description',
      header: 'Equipment Package',
      sortable: true,
      render: (item) => (
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-blue-400">
            <Truck className="h-4 w-4" />
          </div>
          <div>
            <span className="font-semibold text-slate-100">{item.item_description}</span>
            <p className="text-[11px] text-slate-500 font-mono mt-0.5">PO: {item.po_number || 'Pending PO'}</p>
          </div>
        </div>
      ),
    },
    {
      key: 'supplier_name',
      header: 'Supplier / OEM',
      sortable: true,
      render: (item) => <span className="text-slate-300 font-medium">{item.supplier_name}</span>,
    },
    {
      key: 'lead_time_weeks',
      header: 'Lead Time',
      render: (item) => <span className="font-mono text-slate-300">{item.lead_time_weeks} weeks</span>,
    },
    {
      key: 'cost',
      header: 'Package Value',
      render: (item) => (
        <span className="font-mono text-cyan-300 font-bold">
          ${item.cost ? item.cost.toLocaleString() : 'N/A'} {item.currency}
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Delivery Status',
      sortable: true,
      render: (item) => <StatusBadge status={item.status} />,
    },
  ];

  if (isLoading && items.length === 0) {
    return <LoadingState message="Loading long-lead procurement bill of materials..." />;
  }

  if (error && items.length === 0) {
    return <ErrorState message={error} onRetry={loadItems} />;
  }

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Equipment Procurement & Bill of Materials' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <Truck className="h-6 w-6 text-blue-400" />
            Long-Lead Procurement & Delivery Tracker
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Tracking purchase orders, manufacturing lead times, FAT milestones, and port customs clearance.
          </p>
        </div>
      </div>

      <DataTable
        title="Major Equipment Procurement Packages"
        subtitle="Long-lead electrical, mechanical, and life-safety packages"
        columns={columns}
        data={items}
        searchKey={(i) => `${i.item_description} ${i.supplier_name} ${i.po_number}`}
        filterTabs={[
          { label: 'All Items', value: 'all', filterFn: () => true },
          { label: 'Customs Hold', value: 'hold', filterFn: (i) => i.status === 'customs_hold' },
          { label: 'In Transit', value: 'transit', filterFn: (i) => i.status === 'in_transit' },
          { label: 'Delivered', value: 'deliv', filterFn: (i) => i.status === 'delivered' },
        ]}
      />
    </div>
  );
}
"""

# Risks Page
pages['frontend/app/risks/page.tsx'] = """'use client';

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
"""

# Commissioning Page
pages['frontend/app/commissioning/page.tsx'] = """'use client';

import React from 'react';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { StatusBadge } from '@/components/StatusBadge';
import { CheckCircle2, ShieldCheck, Sparkles, Clock } from 'lucide-react';

const mockTests = [
  {
    id: '1',
    level: 'Level 5 - Integrated System IST',
    code: 'IST-ELEC-001',
    name: 'Full Facility Blackout & Generator Auto-Start Synchronization Test',
    criteria: 'All 4 standby diesel generators must start, synchronize, and assume critical load within 10.0 seconds of grid drop.',
    result: 'pending',
    witness: 'Client Third-Party Commissioning Agent (CxA)',
  },
  {
    id: '2',
    level: 'Level 1 - Factory Acceptance (FAT)',
    code: 'FAT-MECH-001',
    name: 'Centrifugal Chiller 500TR Full Load & Part Load Performance Test',
    criteria: 'Verified power input <= 0.545 kW/ton at 100% load and COP >= 6.20 under AHRI 550/590 conditions.',
    result: 'PASS',
    witness: 'Nova MEP Lead Engineer',
  },
  {
    id: '3',
    level: 'Level 4 - Functional System Test',
    code: 'FPT-ELEC-002',
    name: 'UPS Static Bypass & Fault-Clearing Capacity Verification',
    criteria: 'Seamless static transfer to bypass and back without output disturbance exceeding ITIC curve tolerance.',
    result: 'pending',
    witness: 'Electrical Commissioning Director',
  },
];

export default function CommissioningPage() {
  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Quality Records & Level 1-5 Commissioning' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <CheckCircle2 className="h-6 w-6 text-purple-400" />
            Quality & Commissioning Verification Matrix
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Tracking Level 1 (FAT), Level 2 (Site Receipt), Level 3 (Pre-Functional), Level 4 (Functional), and Level 5 Integrated Systems Testing (IST).
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {mockTests.map((test) => (
          <div
            key={test.id}
            className="rounded-xl border border-slate-800 bg-slate-950/60 p-5 space-y-3 hover:border-slate-700 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 px-2 py-0.5 text-[10px] font-mono font-bold uppercase">
                  {test.level}
                </span>
                <span className="font-mono text-cyan-400 text-xs font-bold">{test.code}</span>
              </div>
              <StatusBadge status={test.result} />
            </div>

            <div>
              <h3 className="text-sm font-semibold text-white">{test.name}</h3>
              <p className="text-xs text-slate-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800 mt-2 font-mono">
                Acceptance Criteria: {test.criteria}
              </p>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
              <span>Witness: <strong className="text-slate-300 font-normal">{test.witness}</strong></span>
              <span className="font-mono text-purple-400">ASHRAE Guideline 0-2019</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
"""

# Assistant (RAG Chat Preview)
pages['frontend/app/assistant/page.tsx'] = """'use client';

import React, { useState } from 'react';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { Bot, Send, Sparkles, FileText, CheckCircle2 } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: string[];
}

export default function AssistantPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello Engineer. I am your Data Centre EPC AI Assistant. I have indexed all project specifications, vendor submittals, Primavera P6 schedule networks, and equipment BOMs. Ask me any question about Project Titan DC-01.',
      citations: [],
    },
  ]);
  const [input, setInput] = useState('');

  const samplePrompts = [
    'Why did the UPS submittal fail the specification compliance check?',
    'What is the critical path delay impact of the transformer customs hold?',
    'List the acceptance criteria for Level 5 Integrated Systems Testing (IST).',
    'Compare Chiller COP submittal against ASHRAE 90.4 standard.',
  ];

  const handleSend = (queryText?: string) => {
    const text = queryText || input;
    if (!text.trim()) return;

    const userMsg: Message = { role: 'user', content: text, citations: [] };
    
    // Demo intelligent RAG response based on seed data
    const botResponse: Message = {
      role: 'assistant',
      content: '',
      citations: [],
    };

    if (text.toLowerCase().includes('ups') || text.toLowerCase().includes('fail')) {
      botResponse.content = 'The UPS submittal (SUB-ELEC-UPS-001-Rev1 from Vertiv) was REJECTED with a CRITICAL non-conformance. Contract Specification Section 26 33 53 Paragraph 2.04 mandates a minimum AC-AC double-conversion efficiency of 96.5% at 100% full load. Vertiv submitted 94.0%, resulting in a 2.5% efficiency deficit that increases data centre PUE and dissipates 50kW extra heat per unit into Data Hall 1.';
      botResponse.citations = ['SPEC-ELEC-263353-UPS-V2.pdf (Page 18, Para 2.04)', 'SUB-ELEC-UPS-001-Vertiv-Rev1.pdf'];
    } else if (text.toLowerCase().includes('transformer') || text.toLowerCase().includes('delay') || text.toLowerCase().includes('schedule')) {
      botResponse.content = 'The 33kV/11kV 25MVA Power Transformer (TR-01A / PO-ELEC-2026-004) is currently on customs documentation hold at the Port of Baltimore. This creates an 18-day delay on Activity ACT-1020 (Rigging & Placement). Because ACT-1020 is on the Critical Path, it directly delays Primary Substation Energization (ACT-1050) and Level 5 IST Handover. AI recommends activating the customs priority pre-clearance bond immediately.';
      botResponse.citations = ['Primavera P6 Schedule: ACT-1020', 'PO-ELEC-2026-004 Tracking'];
    } else {
      botResponse.content = 'Based on the Project Titan DC-01 baseline data: All 4 standby diesel generators (GEN-01A) are compliant with NFPA 110 Type 10 standards (8.5s start vs 10.0s requirement). The 500TR Centrifugal Chiller complies with ASHRAE 90.4 with a COP of 6.45.';
      botResponse.citations = ['SPEC-MECH-236416-CHILLER.pdf', 'SPEC-ELEC-263213-GENSET.pdf'];
    }

    setMessages((prev) => [...prev, userMsg, botResponse]);
    setInput('');
  };

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'AI Engineering Assistant (RAG Intelligence)' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
              <Bot className="h-6 w-6 text-cyan-400" />
              AI Project Assistant
            </h1>
            <span className="rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 px-2 py-0.5 text-[10px] font-mono font-bold">
              PHASE 5 PREVIEW
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Grounded RAG question-answering over engineering specifications, submittals, and CPM schedule networks.
          </p>
        </div>
      </div>

      {/* Suggested Prompts */}
      <div className="flex flex-wrap gap-2">
        {samplePrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(prompt)}
            className="text-left px-3 py-1.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800 text-xs text-slate-300 hover:text-white transition-all shadow-sm"
          >
            &ldquo;{prompt}&rdquo;
          </button>
        ))}
      </div>

      {/* Chat Messages Stream */}
      <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4 sm:p-6 min-h-[420px] max-h-[550px] overflow-y-auto space-y-4 custom-scrollbar shadow-inner">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 shrink-0 mt-0.5">
                <Bot className="h-4 w-4" />
              </div>
            )}
            <div
              className={`p-4 rounded-2xl max-w-2xl text-xs space-y-2 leading-relaxed shadow-sm ${
                msg.role === 'user'
                  ? 'bg-cyan-600 text-white font-medium rounded-tr-none'
                  : 'bg-slate-900/80 text-slate-200 border border-slate-800 rounded-tl-none'
              }`}
            >
              <p>{msg.content}</p>
              {msg.citations && msg.citations.length > 0 && (
                <div className="pt-2 border-t border-slate-800/80 space-y-1">
                  <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block">
                    Verified RAG Citations:
                  </span>
                  {msg.citations.map((c, i) => (
                    <div key={i} className="flex items-center gap-1.5 text-[11px] text-slate-400 font-mono">
                      <FileText className="h-3 w-3 text-cyan-400" />
                      <span>{c}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Input Bar */}
      <div className="flex items-center gap-2 p-2 rounded-2xl border border-slate-800 bg-slate-900/80">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a technical specification or critical path question..."
          className="flex-1 bg-transparent px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none"
        />
        <button
          onClick={() => handleSend()}
          className="p-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white shadow-md shadow-cyan-500/20 transition-all"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
"""

for filepath, code in pages.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f'Wrote {filepath} ({len(code)} bytes)')
