'use client';

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
