'use client';

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
