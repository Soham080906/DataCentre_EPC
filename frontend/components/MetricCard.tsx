'use client';

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
