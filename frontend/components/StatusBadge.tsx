'use client';

import React from 'react';
import { cn } from '@/lib/utils';
import { CheckCircle2, AlertTriangle, XCircle, RefreshCw } from 'lucide-react';

interface StatusBadgeProps {
  status: 'healthy' | 'degraded' | 'error' | 'loading';
  text?: string;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, text, className }) => {
  const configs = {
    healthy: {
      bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
      dot: 'bg-emerald-400',
      icon: CheckCircle2,
      label: 'Operational',
    },
    degraded: {
      bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
      dot: 'bg-amber-400',
      icon: AlertTriangle,
      label: 'Degraded',
    },
    error: {
      bg: 'bg-rose-500/10 border-rose-500/30 text-rose-400',
      dot: 'bg-rose-400',
      icon: XCircle,
      label: 'Offline',
    },
    loading: {
      bg: 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400',
      dot: 'bg-cyan-400 animate-ping',
      icon: RefreshCw,
      label: 'Checking...',
    },
  };

  const config = configs[status];
  const Icon = config.icon;

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border backdrop-blur-sm transition-all',
        config.bg,
        className
      )}
    >
      <span className={cn('w-2 h-2 rounded-full', config.dot)} />
      <Icon className={cn('w-3.5 h-3.5', status === 'loading' && 'animate-spin')} />
      <span>{text || config.label}</span>
    </span>
  );
};
