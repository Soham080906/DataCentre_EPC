'use client';

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
