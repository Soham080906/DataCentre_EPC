import os

files = {}

# 1. Breadcrumbs.tsx
files['frontend/components/Breadcrumbs.tsx'] = """'use client';

import React from 'react';
import Link from 'next/link';
import { ChevronRight, Home } from 'lucide-react';

export interface BreadcrumbItem {
  label: string;
  href?: string;
}

interface BreadcrumbsProps {
  items: BreadcrumbItem[];
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({ items }) => {
  return (
    <nav className="flex items-center space-x-1.5 text-xs text-slate-400 mb-4" aria-label="Breadcrumb">
      <Link
        href="/dashboard"
        className="flex items-center gap-1 hover:text-cyan-400 transition-colors py-0.5"
      >
        <Home className="h-3.5 w-3.5 text-slate-500 hover:text-cyan-400" />
        <span className="hidden sm:inline">Dashboard</span>
      </Link>
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        return (
          <React.Fragment key={index}>
            <ChevronRight className="h-3.5 w-3.5 text-slate-600 shrink-0" />
            {isLast || !item.href ? (
              <span className="font-medium text-slate-200 truncate max-w-[200px] sm:max-w-none">
                {item.label}
              </span>
            ) : (
              <Link
                href={item.href}
                className="hover:text-cyan-400 transition-colors truncate max-w-[150px] sm:max-w-none"
              >
                {item.label}
              </Link>
            )}
          </React.Fragment>
        );
      })}
    </nav>
  );
};
"""

# 2. ProjectSelector.tsx
files['frontend/components/ProjectSelector.tsx'] = """'use client';

import React from 'react';
import { useProject } from '@/hooks/useProject';
import { FolderKanban, ChevronDown, Check } from 'lucide-react';

export const ProjectSelector: React.FC = () => {
  const { projects, selectedProject, selectedProjectId, setSelectedProjectId, isLoading } = useProject();
  const [isOpen, setIsOpen] = React.useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (isLoading && projects.length === 0) {
    return (
      <div className="flex items-center gap-2 h-9 px-3 rounded-lg border border-slate-800 bg-slate-900/50 text-xs text-slate-400 animate-pulse">
        <FolderKanban className="h-4 w-4 text-slate-500" />
        <span>Loading project...</span>
      </div>
    );
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 h-9 px-3 rounded-lg border border-slate-800 bg-slate-900/80 hover:bg-slate-800 text-xs font-medium text-slate-200 transition-colors max-w-[260px] sm:max-w-[340px] truncate shadow-sm"
        title="Switch Active EPC Project"
      >
        <FolderKanban className="h-4 w-4 text-cyan-400 shrink-0" />
        <span className="truncate font-semibold text-slate-100">
          {selectedProject ? selectedProject.name : 'Select Project'}
        </span>
        {selectedProject?.code && (
          <span className="hidden sm:inline-block rounded bg-cyan-500/10 px-1.5 py-0.5 text-[10px] font-mono text-cyan-300 border border-cyan-500/20 shrink-0">
            {selectedProject.code}
          </span>
        )}
        <ChevronDown className="h-3.5 w-3.5 text-slate-400 shrink-0 ml-auto" />
      </button>

      {isOpen && (
        <div className="absolute left-0 mt-1 w-80 rounded-xl border border-slate-800 bg-slate-950/95 backdrop-blur-xl p-1.5 shadow-2xl z-50 animate-in fade-in zoom-in-95 duration-100">
          <div className="px-2.5 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800/80 mb-1">
            Active EPC Projects ({projects.length})
          </div>
          <div className="max-h-60 overflow-y-auto space-y-0.5 custom-scrollbar">
            {projects.map((proj) => {
              const isSelected = proj.id === selectedProjectId;
              return (
                <button
                  key={proj.id}
                  onClick={() => {
                    setSelectedProjectId(proj.id);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-start gap-2.5 px-2.5 py-2 rounded-lg text-left text-xs transition-colors ${
                    isSelected
                      ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 font-medium'
                      : 'text-slate-300 hover:bg-slate-900 hover:text-white'
                  }`}
                >
                  <div className="mt-0.5 shrink-0">
                    {isSelected ? (
                      <Check className="h-3.5 w-3.5 text-cyan-400" />
                    ) : (
                      <div className="h-3.5 w-3.5 rounded-full border border-slate-700" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-1">
                      <span className="font-medium truncate">{proj.name}</span>
                      <span className="font-mono text-[10px] text-slate-400 shrink-0">{proj.code}</span>
                    </div>
                    {proj.location && (
                      <p className="text-[11px] text-slate-500 truncate mt-0.5">{proj.location}</p>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
"""

# 3. StatusBadge.tsx
files['frontend/components/StatusBadge.tsx'] = """'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { CheckCircle2, XCircle, AlertTriangle, Clock, RefreshCw, ShieldAlert, Sparkles } from 'lucide-react';

export type StatusVariant =
  | 'healthy'
  | 'degraded'
  | 'error'
  | 'loading'
  | 'PASS'
  | 'FAIL'
  | 'WARNING'
  | 'CRITICAL'
  | 'HIGH'
  | 'MEDIUM'
  | 'LOW'
  | 'DELAYED'
  | 'IN_PROGRESS'
  | 'COMPLETED'
  | 'NOT_STARTED'
  | 'CUSTOMS_HOLD'
  | 'FAT_PASSED'
  | 'IN_TRANSIT'
  | 'DELIVERED'
  | 'OPEN'
  | 'ANSWERED';

interface StatusBadgeProps {
  status: string;
  text?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  showIcon?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  text,
  size = 'md',
  className,
  showIcon = true,
}) => {
  const normalized = status.toUpperCase().replace(/\\s+/g, '_');

  const getStyles = () => {
    switch (normalized) {
      case 'HEALTHY':
      case 'PASS':
      case 'COMPLETED':
      case 'DELIVERED':
      case 'FAT_PASSED':
      case 'ANSWERED':
        return {
          bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
          dot: 'bg-emerald-400',
          icon: CheckCircle2,
        };
      case 'FAIL':
      case 'CRITICAL':
      case 'ERROR':
        return {
          bg: 'bg-rose-500/15 text-rose-400 border-rose-500/30',
          dot: 'bg-rose-400',
          icon: XCircle,
        };
      case 'HIGH':
      case 'DELAYED':
      case 'CUSTOMS_HOLD':
        return {
          bg: 'bg-orange-500/15 text-orange-400 border-orange-500/30',
          dot: 'bg-orange-400',
          icon: ShieldAlert,
        };
      case 'DEGRADED':
      case 'WARNING':
      case 'MEDIUM':
        return {
          bg: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
          dot: 'bg-amber-400',
          icon: AlertTriangle,
        };
      case 'IN_PROGRESS':
      case 'IN_TRANSIT':
      case 'OPEN':
      case 'LOADING':
        return {
          bg: 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30',
          dot: 'bg-cyan-400 animate-pulse',
          icon: RefreshCw,
        };
      case 'LOW':
      case 'NOT_STARTED':
      default:
        return {
          bg: 'bg-slate-800/80 text-slate-300 border-slate-700/60',
          dot: 'bg-slate-400',
          icon: Clock,
        };
    }
  };

  const style = getStyles();
  const IconComponent = style.icon;

  const sizeClasses = {
    sm: 'px-1.5 py-0.5 text-[10px] gap-1',
    md: 'px-2 py-0.5 text-xs gap-1.5',
    lg: 'px-2.5 py-1 text-xs font-semibold gap-2',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center rounded-md border font-medium uppercase tracking-wider transition-colors',
        style.bg,
        sizeClasses[size],
        className
      )}
    >
      {showIcon && <IconComponent className="h-3 w-3 shrink-0" />}
      <span>{text || status.replace(/_/g, ' ')}</span>
    </span>
  );
};
"""

# 4. MetricCard.tsx
files['frontend/components/MetricCard.tsx'] = """'use client';

import React from 'react';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: {
    value: string;
    isPositive?: boolean;
    label?: string;
  };
  variant?: 'cyan' | 'blue' | 'emerald' | 'amber' | 'rose' | 'slate';
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  variant = 'cyan',
  className,
}) => {
  const variantStyles = {
    cyan: 'from-cyan-500/10 to-blue-500/5 border-cyan-500/20 text-cyan-400 icon-bg-cyan-500/15',
    blue: 'from-blue-500/10 to-indigo-500/5 border-blue-500/20 text-blue-400 icon-bg-blue-500/15',
    emerald: 'from-emerald-500/10 to-teal-500/5 border-emerald-500/20 text-emerald-400 icon-bg-emerald-500/15',
    amber: 'from-amber-500/10 to-yellow-500/5 border-amber-500/20 text-amber-400 icon-bg-amber-500/15',
    rose: 'from-rose-500/10 to-pink-500/5 border-rose-500/20 text-rose-400 icon-bg-rose-500/15',
    slate: 'from-slate-800/40 to-slate-900/40 border-slate-800 text-slate-300 icon-bg-slate-800',
  };

  return (
    <div
      className={cn(
        'relative overflow-hidden rounded-xl border bg-gradient-to-br p-5 shadow-sm transition-all duration-200 hover:border-slate-700/80 bg-slate-950/60 backdrop-blur-sm',
        variantStyles[variant],
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">{title}</p>
          <p className="mt-2 text-2xl font-bold tracking-tight text-white font-mono">{value}</p>
          {subtitle && <p className="mt-1 text-xs text-slate-400">{subtitle}</p>}
        </div>
        <div className="rounded-lg p-2.5 bg-slate-900/80 border border-slate-800 text-slate-200 shadow-inner">
          <Icon className="h-5 w-5" />
        </div>
      </div>

      {trend && (
        <div className="mt-3 flex items-center gap-1.5 text-xs">
          <span
            className={cn(
              'font-semibold px-1.5 py-0.5 rounded text-[11px]',
              trend.isPositive
                ? 'bg-emerald-500/15 text-emerald-400'
                : 'bg-rose-500/15 text-rose-400'
            )}
          >
            {trend.value}
          </span>
          {trend.label && <span className="text-slate-500">{trend.label}</span>}
        </div>
      )}
    </div>
  );
};
"""

# 5. HealthGaugeCard.tsx
files['frontend/components/HealthGaugeCard.tsx'] = """'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { Activity, ShieldCheck, Truck, Calendar, CheckCircle2 } from 'lucide-react';

interface HealthGaugeProps {
  label: string;
  score: number;
  category: 'schedule' | 'procurement' | 'quality' | 'commissioning';
  statusText?: string;
  subtitle?: string;
}

export const HealthGaugeCard: React.FC<HealthGaugeProps> = ({
  label,
  score,
  category,
  statusText,
  subtitle,
}) => {
  const getCategoryMeta = () => {
    switch (category) {
      case 'schedule':
        return { icon: Calendar, color: 'cyan', title: 'Schedule Health' };
      case 'procurement':
        return { icon: Truck, color: 'blue', title: 'Procurement Health' };
      case 'quality':
        return { icon: ShieldCheck, color: 'emerald', title: 'Quality & Spec Health' };
      case 'commissioning':
        return { icon: CheckCircle2, color: 'purple', title: 'Commissioning Readiness' };
    }
  };

  const meta = getCategoryMeta();
  const Icon = meta.icon;

  const getScoreColor = (val: number) => {
    if (val >= 80) return 'text-emerald-400 stroke-emerald-400 bg-emerald-500/15 border-emerald-500/30';
    if (val >= 60) return 'text-amber-400 stroke-amber-400 bg-amber-500/15 border-amber-500/30';
    return 'text-rose-400 stroke-rose-400 bg-rose-500/15 border-rose-500/30';
  };

  const scoreClass = getScoreColor(score);

  return (
    <div className="rounded-xl border border-slate-800/80 bg-slate-950/70 p-4 shadow-sm hover:border-slate-700 transition-colors">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="rounded-lg p-2 bg-slate-900 border border-slate-800 text-slate-300">
            <Icon className="h-4 w-4" />
          </div>
          <div>
            <h4 className="text-xs font-semibold text-slate-200">{label}</h4>
            <p className="text-[11px] text-slate-500">{subtitle || meta.title}</p>
          </div>
        </div>
        <div className="flex items-baseline gap-1">
          <span className="text-xl font-bold font-mono text-white">{score}%</span>
        </div>
      </div>

      {/* Industrial Progress Bar */}
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-900 border border-slate-800/80 p-0.5">
        <div
          className={cn(
            'h-full rounded-full transition-all duration-500',
            score >= 80 ? 'bg-gradient-to-r from-emerald-500 to-teal-400' : score >= 60 ? 'bg-gradient-to-r from-amber-500 to-yellow-400' : 'bg-gradient-to-r from-rose-500 to-red-400'
          )}
          style={{ width: `${Math.max(5, Math.min(100, score))}%` }}
        />
      </div>

      <div className="mt-2.5 flex items-center justify-between text-[11px]">
        <span className="text-slate-500">Status</span>
        <span
          className={cn(
            'rounded px-1.5 py-0.2 font-medium font-mono text-[10px] uppercase border',
            scoreClass
          )}
        >
          {statusText || (score >= 80 ? 'OPTIMAL' : score >= 60 ? 'WATCHLIST' : 'ACTION REQUIRED')}
        </span>
      </div>
    </div>
  );
};
"""

# 6. AlertBanner.tsx
files['frontend/components/AlertBanner.tsx'] = """'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { AlertCircle, AlertTriangle, Info, CheckCircle2, ChevronRight } from 'lucide-react';
import Link from 'next/link';

interface AlertBannerProps {
  title: string;
  message?: string;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
  actionHref?: string;
  actionText?: string;
  className?: string;
}

export const AlertBanner: React.FC<AlertBannerProps> = ({
  title,
  message,
  severity,
  actionHref,
  actionText = 'Review Details',
  className,
}) => {
  const getSeverityStyles = () => {
    switch (severity) {
      case 'critical':
        return {
          bg: 'bg-rose-950/40 border-rose-800/60 text-rose-200',
          icon: AlertCircle,
          iconColor: 'text-rose-400',
          badge: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
        };
      case 'high':
        return {
          bg: 'bg-orange-950/40 border-orange-800/60 text-orange-200',
          icon: AlertTriangle,
          iconColor: 'text-orange-400',
          badge: 'bg-orange-500/20 text-orange-300 border-orange-500/30',
        };
      case 'medium':
        return {
          bg: 'bg-amber-950/40 border-amber-800/60 text-amber-200',
          icon: AlertTriangle,
          iconColor: 'text-amber-400',
          badge: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
        };
      case 'low':
      case 'info':
      default:
        return {
          bg: 'bg-cyan-950/30 border-cyan-800/50 text-cyan-200',
          icon: Info,
          iconColor: 'text-cyan-400',
          badge: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
        };
    }
  };

  const style = getSeverityStyles();
  const Icon = style.icon;

  return (
    <div
      className={cn(
        'flex items-start sm:items-center justify-between gap-3 rounded-xl border p-3.5 text-xs shadow-sm backdrop-blur-sm transition-all',
        style.bg,
        className
      )}
    >
      <div className="flex items-start sm:items-center gap-3">
        <Icon className={cn('h-4 w-4 shrink-0 mt-0.5 sm:mt-0', style.iconColor)} />
        <div>
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-100">{title}</span>
            <span
              className={cn(
                'rounded px-1.5 py-0.2 text-[10px] font-mono uppercase font-bold border',
                style.badge
              )}
            >
              {severity}
            </span>
          </div>
          {message && <p className="mt-0.5 text-slate-300/90 text-xs">{message}</p>}
        </div>
      </div>

      {actionHref && (
        <Link
          href={actionHref}
          className="flex items-center gap-1 shrink-0 rounded-lg px-2.5 py-1.5 bg-slate-900/80 hover:bg-slate-800 border border-slate-700 text-[11px] font-medium text-slate-200 hover:text-white transition-colors"
        >
          <span>{actionText}</span>
          <ChevronRight className="h-3 w-3" />
        </Link>
      )}
    </div>
  );
};
"""

# 7. DataTable.tsx
files['frontend/components/DataTable.tsx'] = """'use client';

import React, { useState, useMemo } from 'react';
import { Search, ChevronDown, ChevronUp, SlidersHorizontal, FileSpreadsheet } from 'lucide-react';
import { cn } from '@/lib/utils';
import { EmptyState } from './EmptyState';

export interface Column<T> {
  key: string;
  header: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  searchPlaceholder?: string;
  searchKey?: keyof T | ((item: T) => string);
  filterTabs?: { label: string; value: string; filterFn: (item: T) => boolean }[];
  title?: string;
  subtitle?: string;
  actions?: React.ReactNode;
  emptyTitle?: string;
  emptyMessage?: string;
}

export function DataTable<T extends Record<string, any>>({
  columns,
  data,
  searchPlaceholder = 'Search records...',
  searchKey,
  filterTabs,
  title,
  subtitle,
  actions,
  emptyTitle = 'No records found',
  emptyMessage = 'No matching data entries found for current criteria.',
}: DataTableProps<T>) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeTab, setActiveTab] = useState(0);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);

  const filteredData = useMemo(() => {
    let result = [...data];

    // Apply tab filters
    if (filterTabs && filterTabs[activeTab]) {
      result = result.filter(filterTabs[activeTab].filterFn);
    }

    // Apply search
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter((item) => {
        if (typeof searchKey === 'function') {
          return searchKey(item).toLowerCase().includes(q);
        } else if (searchKey && item[searchKey]) {
          return String(item[searchKey]).toLowerCase().includes(q);
        }
        // Fallback: search all values
        return Object.values(item).some(
          (val) => val !== null && val !== undefined && String(val).toLowerCase().includes(q)
        );
      });
    }

    // Apply sorting
    if (sortConfig) {
      result.sort((a, b) => {
        const aVal = a[sortConfig.key];
        const bVal = b[sortConfig.key];
        if (aVal === bVal) return 0;
        if (aVal === null || aVal === undefined) return 1;
        if (bVal === null || bVal === undefined) return -1;

        if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
        return sortConfig.direction === 'asc' ? 1 : -1;
      });
    }

    return result;
  }, [data, filterTabs, activeTab, searchQuery, searchKey, sortConfig]);

  const handleSort = (key: string) => {
    setSortConfig((prev) => {
      if (prev?.key === key) {
        if (prev.direction === 'asc') return { key, direction: 'desc' };
        return null;
      }
      return { key, direction: 'asc' };
    });
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-950/60 backdrop-blur-md overflow-hidden shadow-sm">
      {/* Table Header Controls */}
      <div className="p-4 border-b border-slate-800/80 space-y-3 sm:space-y-0 sm:flex sm:items-center sm:justify-between gap-4">
        <div>
          {title && <h3 className="text-sm font-semibold text-slate-100">{title}</h3>}
          {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          {/* Search Bar */}
          <div className="relative min-w-[220px]">
            <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-slate-500" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={searchPlaceholder}
              className="w-full h-8 pl-8 pr-3 rounded-lg border border-slate-800 bg-slate-900/80 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors"
            />
          </div>
          {actions}
        </div>
      </div>

      {/* Filter Tabs if available */}
      {filterTabs && filterTabs.length > 0 && (
        <div className="px-4 py-2 border-b border-slate-800/60 flex items-center gap-1.5 overflow-x-auto custom-scrollbar">
          {filterTabs.map((tab, idx) => (
            <button
              key={tab.label}
              onClick={() => setActiveTab(idx)}
              className={cn(
                'px-3 py-1 rounded-lg text-xs font-medium transition-colors shrink-0',
                activeTab === idx
                  ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              )}
            >
              {tab.label}
            </button>
          ))}
        </div>
      )}

      {/* Table Component */}
      <div className="overflow-x-auto custom-scrollbar">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-800/80 bg-slate-900/40 text-slate-400">
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => col.sortable && handleSort(col.key)}
                  className={cn(
                    'py-3 px-4 font-semibold uppercase tracking-wider text-[11px]',
                    col.sortable && 'cursor-pointer select-none hover:text-slate-200',
                    col.className
                  )}
                >
                  <div className="flex items-center gap-1">
                    <span>{col.header}</span>
                    {col.sortable && sortConfig?.key === col.key && (
                      sortConfig.direction === 'asc' ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50">
            {filteredData.length > 0 ? (
              filteredData.map((item, rowIdx) => (
                <tr
                  key={item.id || rowIdx}
                  className="hover:bg-slate-900/40 transition-colors group"
                >
                  {columns.map((col) => (
                    <td key={col.key} className={cn('py-3 px-4 text-slate-300', col.className)}>
                      {col.render ? col.render(item) : item[col.key]}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length} className="py-12">
                  <EmptyState
                    title={emptyTitle}
                    description={emptyMessage}
                    icon={FileSpreadsheet}
                  />
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Table Footer */}
      <div className="px-4 py-2.5 border-t border-slate-800/80 bg-slate-900/30 flex items-center justify-between text-[11px] text-slate-500 font-mono">
        <span>Showing {filteredData.length} of {data.length} records</span>
      </div>
    </div>
  );
}
"""

# 8. LoadingState.tsx
files['frontend/components/LoadingState.tsx'] = """'use client';

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
"""

# 9. EmptyState.tsx
files['frontend/components/EmptyState.tsx'] = """'use client';

import React from 'react';
import { LucideIcon, FolderSearch } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
  icon?: LucideIcon;
  actionText?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No Data Available',
  description = 'No active records or telemetry detected for this module.',
  icon: Icon = FolderSearch,
  actionText,
  onAction,
}) => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 rounded-xl border border-dashed border-slate-800 bg-slate-950/30 min-h-[220px]">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-900/80 border border-slate-800 text-slate-400 shadow-inner">
        <Icon className="h-6 w-6" />
      </div>
      <h4 className="mt-3 text-sm font-semibold text-slate-200">{title}</h4>
      <p className="mt-1 text-xs text-slate-500 max-w-sm">{description}</p>
      {actionText && onAction && (
        <button
          onClick={onAction}
          className="mt-4 px-3.5 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-medium shadow-md shadow-cyan-500/20 transition-all"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};
"""

# 10. ErrorState.tsx
files['frontend/components/ErrorState.tsx'] = """'use client';

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
"""

# 11. Navbar.tsx (Enhanced)
files['frontend/components/Navbar.tsx'] = """'use client';

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
"""

# 12. Sidebar.tsx (Enhanced)
files['frontend/components/Sidebar.tsx'] = """'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
  LayoutDashboard,
  FileText,
  Bot,
  ShieldCheck,
  CalendarDays,
  Truck,
  AlertOctagon,
  CheckCircle2,
  Cpu,
} from 'lucide-react';

const navigationItems = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard, badge: 'Live' },
  { name: 'Documents & Specs', href: '/documents', icon: FileText, badge: '3 Docs' },
  { name: 'AI Assistant', href: '/assistant', icon: Bot, badge: 'RAG' },
  { name: 'Spec Compliance', href: '/compliance', icon: ShieldCheck, badge: '1 Fail' },
  { name: 'Schedule CPM', href: '/schedule', icon: CalendarDays, badge: 'Critical' },
  { name: 'Procurement BOM', href: '/procurement', icon: Truck, badge: 'Customs' },
  { name: 'Risk Analytics', href: '/risks', icon: AlertOctagon, badge: '2 Active' },
  { name: 'Commissioning', href: '/commissioning', icon: CheckCircle2, badge: 'Level 1-5' },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950/60 p-4 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="space-y-6">
        <div>
          <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
            EPC Intelligence Modules
          </p>
          <nav className="mt-2.5 space-y-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || (item.href === '/dashboard' && pathname === '/');
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    'group flex items-center justify-between rounded-xl px-3 py-2.5 text-xs font-medium transition-all duration-150',
                    isActive
                      ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 shadow-sm shadow-cyan-500/5'
                      : 'text-slate-400 hover:bg-slate-900/80 hover:text-slate-100'
                  )}
                >
                  <div className="flex items-center gap-3">
                    <Icon
                      className={cn(
                        'h-4 w-4 transition-colors',
                        isActive ? 'text-cyan-400' : 'text-slate-500 group-hover:text-slate-300'
                      )}
                    />
                    <span>{item.name}</span>
                  </div>
                  {item.badge && (
                    <span
                      className={cn(
                        'rounded px-1.5 py-0.2 text-[9px] font-mono uppercase font-bold tracking-wider',
                        isActive
                          ? 'bg-cyan-500/25 text-cyan-200 border border-cyan-500/30'
                          : 'bg-slate-900 text-slate-400 border border-slate-800'
                      )}
                    >
                      {item.badge}
                    </span>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Industrial Spec Footer */}
      <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-3 text-xs">
        <div className="flex items-center justify-between text-slate-400">
          <span className="font-semibold text-slate-200 flex items-center gap-1">
            <Cpu className="h-3 w-3 text-cyan-400" />
            Project Titan DC-01
          </span>
          <span className="font-mono text-cyan-400 text-[10px]">50MW</span>
        </div>
        <p className="mt-1 text-[11px] text-slate-500">
          Tier III 2N / N+1 Hyperscale EPC
        </p>
      </div>
    </aside>
  );
};
"""

for filepath, code in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f'Wrote {filepath} ({len(code)} bytes)')
