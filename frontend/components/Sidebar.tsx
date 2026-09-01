'use client';

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
  CheckCircle,
} from 'lucide-react';

const navigationItems = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard, badge: 'Overview' },
  { name: 'Documents & Specs', href: '#documents', icon: FileText, badge: 'Phase 4' },
  { name: 'AI Assistant (RAG)', href: '#assistant', icon: Bot, badge: 'Phase 5' },
  { name: 'Spec Compliance', href: '#compliance', icon: ShieldCheck, badge: 'Phase 6' },
  { name: 'Schedule Risk', href: '#schedule', icon: CalendarDays, badge: 'Phase 7' },
  { name: 'Procurement', href: '#procurement', icon: Truck, badge: 'Phase 7' },
  { name: 'Risk Analytics', href: '#risks', icon: AlertOctagon, badge: 'Phase 7' },
  { name: 'Commissioning', href: '#commissioning', icon: CheckCircle, badge: 'Phase 9' },
];

export const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950/40 p-4 flex flex-col justify-between shrink-0 min-h-[calc(100vh-4rem)]">
      <div className="space-y-6">
        <div>
          <p className="px-3 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
            Intelligence Modules
          </p>
          <nav className="mt-2 space-y-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    'group flex items-center justify-between rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-150',
                    isActive
                      ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-sm shadow-cyan-500/5'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                  )}
                >
                  <div className="flex items-center gap-3">
                    <Icon
                      className={cn(
                        'h-4 w-4 transition-colors',
                        isActive ? 'text-cyan-400' : 'text-slate-400 group-hover:text-slate-200'
                      )}
                    />
                    <span>{item.name}</span>
                  </div>
                  {item.badge && (
                    <span
                      className={cn(
                        'rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider',
                        isActive
                          ? 'bg-cyan-500/20 text-cyan-300'
                          : 'bg-slate-800/80 text-slate-400'
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

      <div className="rounded-lg border border-slate-800/80 bg-slate-900/40 p-3 text-xs">
        <div className="flex items-center justify-between text-slate-400">
          <span>Project MVP</span>
          <span className="font-mono text-cyan-400">Phase 1</span>
        </div>
        <p className="mt-1 text-[11px] text-slate-500">
          Scaffolding & Systems Online
        </p>
      </div>
    </aside>
  );
};
