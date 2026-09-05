'use client';

import React from 'react';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { StatusBadge } from '@/components/StatusBadge';
import { CheckCircle2, ShieldCheck, Sparkles, Clock } from 'lucide-react';

const mockTests = [
  {
    id: '1',
    level: 'Level 5 - Integrated System IST',
    code: 'IST-ELEC-001',
    name: 'Full Facility Blackout & Generator Auto-Start Synchronization Test',
    criteria: 'All 4 standby diesel generators must start, synchronize, and assume critical load within 10.0 seconds of grid drop.',
    result: 'pending',
    witness: 'Client Third-Party Commissioning Agent (CxA)',
  },
  {
    id: '2',
    level: 'Level 1 - Factory Acceptance (FAT)',
    code: 'FAT-MECH-001',
    name: 'Centrifugal Chiller 500TR Full Load & Part Load Performance Test',
    criteria: 'Verified power input <= 0.545 kW/ton at 100% load and COP >= 6.20 under AHRI 550/590 conditions.',
    result: 'PASS',
    witness: 'Nova MEP Lead Engineer',
  },
  {
    id: '3',
    level: 'Level 4 - Functional System Test',
    code: 'FPT-ELEC-002',
    name: 'UPS Static Bypass & Fault-Clearing Capacity Verification',
    criteria: 'Seamless static transfer to bypass and back without output disturbance exceeding ITIC curve tolerance.',
    result: 'pending',
    witness: 'Electrical Commissioning Director',
  },
];

export default function CommissioningPage() {
  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Quality Records & Level 1-5 Commissioning' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
            <CheckCircle2 className="h-6 w-6 text-purple-400" />
            Quality & Commissioning Verification Matrix
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Tracking Level 1 (FAT), Level 2 (Site Receipt), Level 3 (Pre-Functional), Level 4 (Functional), and Level 5 Integrated Systems Testing (IST).
          </p>
        </div>
      </div>

      <div className="space-y-3">
        {mockTests.map((test) => (
          <div
            key={test.id}
            className="rounded-xl border border-slate-800 bg-slate-950/60 p-5 space-y-3 hover:border-slate-700 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="rounded bg-purple-500/10 text-purple-300 border border-purple-500/20 px-2 py-0.5 text-[10px] font-mono font-bold uppercase">
                  {test.level}
                </span>
                <span className="font-mono text-cyan-400 text-xs font-bold">{test.code}</span>
              </div>
              <StatusBadge status={test.result} />
            </div>

            <div>
              <h3 className="text-sm font-semibold text-white">{test.name}</h3>
              <p className="text-xs text-slate-300 bg-slate-900/60 p-3 rounded-lg border border-slate-800 mt-2 font-mono">
                Acceptance Criteria: {test.criteria}
              </p>
            </div>

            <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
              <span>Witness: <strong className="text-slate-300 font-normal">{test.witness}</strong></span>
              <span className="font-mono text-purple-400">ASHRAE Guideline 0-2019</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
