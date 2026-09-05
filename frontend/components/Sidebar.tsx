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
