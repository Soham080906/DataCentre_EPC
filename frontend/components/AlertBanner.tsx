'use client';

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
