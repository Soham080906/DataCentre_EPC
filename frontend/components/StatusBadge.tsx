'use client';

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
  const normalized = status.toUpperCase().replace(/\s+/g, '_');

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
