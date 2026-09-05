'use client';

import React, { useState } from 'react';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { Bot, Send, Sparkles, FileText, CheckCircle2 } from 'lucide-react';

export default function AssistantPage() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello Engineer. I am your Data Centre EPC AI Assistant. I have indexed all project specifications, vendor submittals, Primavera P6 schedule networks, and equipment BOMs. Ask me any question about Project Titan DC-01.',
      citations: [],
    },
  ]);
  const [input, setInput] = useState('');

  const samplePrompts = [
    'Why did the UPS submittal fail the specification compliance check?',
    'What is the critical path delay impact of the transformer customs hold?',
    'List the acceptance criteria for Level 5 Integrated Systems Testing (IST).',
    'Compare Chiller COP submittal against ASHRAE 90.4 standard.',
  ];

  const handleSend = (queryText?: string) => {
    const text = queryText || input;
    if (!text.trim()) return;

    const userMsg = { role: 'user', content: text, citations: [] };
    
    // Demo intelligent RAG response based on seed data
    let botResponse = {
      role: 'assistant',
      content: '',
      citations: [] as string[],
    };

    if (text.toLowerCase().includes('ups') || text.toLowerCase().includes('fail')) {
      botResponse.content = 'The UPS submittal (SUB-ELEC-UPS-001-Rev1 from Vertiv) was REJECTED with a CRITICAL non-conformance. Contract Specification Section 26 33 53 Paragraph 2.04 mandates a minimum AC-AC double-conversion efficiency of 96.5% at 100% full load. Vertiv submitted 94.0%, resulting in a 2.5% efficiency deficit that increases data centre PUE and dissipates 50kW extra heat per unit into Data Hall 1.';
      botResponse.citations = ['SPEC-ELEC-263353-UPS-V2.pdf (Page 18, Para 2.04)', 'SUB-ELEC-UPS-001-Vertiv-Rev1.pdf'];
    } else if (text.toLowerCase().includes('transformer') || text.toLowerCase().includes('delay') || text.toLowerCase().includes('schedule')) {
      botResponse.content = 'The 33kV/11kV 25MVA Power Transformer (TR-01A / PO-ELEC-2026-004) is currently on customs documentation hold at the Port of Baltimore. This creates an 18-day delay on Activity ACT-1020 (Rigging & Placement). Because ACT-1020 is on the Critical Path, it directly delays Primary Substation Energization (ACT-1050) and Level 5 IST Handover. AI recommends activating the customs priority pre-clearance bond immediately.';
      botResponse.citations = ['Primavera P6 Schedule: ACT-1020', 'PO-ELEC-2026-004 Tracking'];
    } else {
      botResponse.content = 'Based on the Project Titan DC-01 baseline data: All 4 standby diesel generators (GEN-01A) are compliant with NFPA 110 Type 10 standards (8.5s start vs 10.0s requirement). The 500TR Centrifugal Chiller complies with ASHRAE 90.4 with a COP of 6.45.';
      botResponse.citations = ['SPEC-MECH-236416-CHILLER.pdf', 'SPEC-ELEC-263213-GENSET.pdf'];
    }

    setMessages((prev) => [...prev, userMsg, botResponse]);
    setInput('');
  };

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'AI Engineering Assistant (RAG Intelligence)' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white flex items-center gap-2.5">
              <Bot className="h-6 w-6 text-cyan-400" />
              AI Project Assistant
            </h1>
            <span className="rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20 px-2 py-0.5 text-[10px] font-mono font-bold">
              PHASE 5 PREVIEW
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Grounded RAG question-answering over engineering specifications, submittals, and CPM schedule networks.
          </p>
        </div>
      </div>

      {/* Suggested Prompts */}
      <div className="flex flex-wrap gap-2">
        {samplePrompts.map((prompt, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(prompt)}
            className="text-left px-3 py-1.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800 text-xs text-slate-300 hover:text-white transition-all shadow-sm"
          >
            &ldquo;{prompt}&rdquo;
          </button>
        ))}
      </div>

      {/* Chat Messages Stream */}
      <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4 sm:p-6 min-h-[420px] max-h-[550px] overflow-y-auto space-y-4 custom-scrollbar shadow-inner">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.role === 'assistant' && (
              <div className="p-2 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 shrink-0 mt-0.5">
                <Bot className="h-4 w-4" />
              </div>
            )}
            <div
              className={`p-4 rounded-2xl max-w-2xl text-xs space-y-2 leading-relaxed shadow-sm ${
                msg.role === 'user'
                  ? 'bg-cyan-600 text-white font-medium rounded-tr-none'
                  : 'bg-slate-900/80 text-slate-200 border border-slate-800 rounded-tl-none'
              }`}
            >
              <p>{msg.content}</p>
              {msg.citations && msg.citations.length > 0 && (
                <div className="pt-2 border-t border-slate-800/80 space-y-1">
                  <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase tracking-wider block">
                    Verified RAG Citations:
                  </span>
                  {msg.citations.map((c, i) => (
                    <div key={i} className="flex items-center gap-1.5 text-[11px] text-slate-400 font-mono">
                      <FileText className="h-3 w-3 text-cyan-400" />
                      <span>{c}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Input Bar */}
      <div className="flex items-center gap-2 p-2 rounded-2xl border border-slate-800 bg-slate-900/80">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask a technical specification or critical path question..."
          className="flex-1 bg-transparent px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none"
        />
        <button
          onClick={() => handleSend()}
          className="p-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white shadow-md shadow-cyan-500/20 transition-all"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
