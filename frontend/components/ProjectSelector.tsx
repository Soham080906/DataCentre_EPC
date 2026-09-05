'use client';

import React from 'react';
import { useProject } from '@/hooks/useProject';
import { FolderKanban, ChevronDown, Check } from 'lucide-react';

export const ProjectSelector: React.FC = () => {
  const { projects, selectedProject, selectedProjectId, setSelectedProjectId, isLoading } = useProject();
  const [isOpen, setIsOpen] = React.useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  if (isLoading && projects.length === 0) {
    return (
      <div className="flex items-center gap-2 h-9 px-3 rounded-lg border border-slate-800 bg-slate-900/50 text-xs text-slate-400 animate-pulse">
        <FolderKanban className="h-4 w-4 text-slate-500" />
        <span>Loading project...</span>
      </div>
    );
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 h-9 px-3 rounded-lg border border-slate-800 bg-slate-900/80 hover:bg-slate-800 text-xs font-medium text-slate-200 transition-colors max-w-[260px] sm:max-w-[340px] truncate shadow-sm"
        title="Switch Active EPC Project"
      >
        <FolderKanban className="h-4 w-4 text-cyan-400 shrink-0" />
        <span className="truncate font-semibold text-slate-100">
          {selectedProject ? selectedProject.name : 'Select Project'}
        </span>
        {selectedProject?.code && (
          <span className="hidden sm:inline-block rounded bg-cyan-500/10 px-1.5 py-0.5 text-[10px] font-mono text-cyan-300 border border-cyan-500/20 shrink-0">
            {selectedProject.code}
          </span>
        )}
        <ChevronDown className="h-3.5 w-3.5 text-slate-400 shrink-0 ml-auto" />
      </button>

      {isOpen && (
        <div className="absolute left-0 mt-1 w-80 rounded-xl border border-slate-800 bg-slate-950/95 backdrop-blur-xl p-1.5 shadow-2xl z-50 animate-in fade-in zoom-in-95 duration-100">
          <div className="px-2.5 py-1.5 text-[11px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800/80 mb-1">
            Active EPC Projects ({projects.length})
          </div>
          <div className="max-h-60 overflow-y-auto space-y-0.5 custom-scrollbar">
            {projects.map((proj) => {
              const isSelected = proj.id === selectedProjectId;
              return (
                <button
                  key={proj.id}
                  onClick={() => {
                    setSelectedProjectId(proj.id);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-start gap-2.5 px-2.5 py-2 rounded-lg text-left text-xs transition-colors ${
                    isSelected
                      ? 'bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 font-medium'
                      : 'text-slate-300 hover:bg-slate-900 hover:text-white'
                  }`}
                >
                  <div className="mt-0.5 shrink-0">
                    {isSelected ? (
                      <Check className="h-3.5 w-3.5 text-cyan-400" />
                    ) : (
                      <div className="h-3.5 w-3.5 rounded-full border border-slate-700" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between gap-1">
                      <span className="font-medium truncate">{proj.name}</span>
                      <span className="font-mono text-[10px] text-slate-400 shrink-0">{proj.code}</span>
                    </div>
                    {proj.location && (
                      <p className="text-[11px] text-slate-500 truncate mt-0.5">{proj.location}</p>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
