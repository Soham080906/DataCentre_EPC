'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { useProject } from '@/hooks/useProject';
import { fetchDocuments, fetchDocumentChunks } from '@/lib/api';
import { Document, DocumentChunk } from '@/types';
import { Breadcrumbs } from '@/components/Breadcrumbs';
import { DataTable, Column } from '@/components/DataTable';
import { StatusBadge } from '@/components/StatusBadge';
import { LoadingState } from '@/components/LoadingState';
import { ErrorState } from '@/components/ErrorState';
import { FileText, Eye, Layers, FileCode, CheckCircle, Clock } from 'lucide-react';

export default function DocumentsPage() {
  const { selectedProjectId } = useProject();
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [chunks, setChunks] = useState<DocumentChunk[]>([]);
  const [loadingChunks, setLoadingChunks] = useState<boolean>(false);

  const loadDocuments = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await fetchDocuments(selectedProjectId || undefined);
      setDocuments(data);
    } catch (err: any) {
      console.error('Failed to load documents:', err);
      setError(err?.message || 'Failed to fetch project documents');
    } finally {
      setIsLoading(false);
    }
  }, [selectedProjectId]);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const handleInspectChunks = async (doc: Document) => {
    setSelectedDoc(doc);
    try {
      setLoadingChunks(true);
      const data = await fetchDocumentChunks(doc.id);
      setChunks(data);
    } catch (err) {
      console.error('Failed to load chunks:', err);
    } finally {
      setLoadingChunks(false);
    }
  };

  const columns: Column<Document>[] = [
    {
      key: 'filename',
      header: 'Document Name',
      sortable: true,
      render: (doc) => (
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-cyan-400">
            <FileText className="h-4 w-4" />
          </div>
          <div>
            <span className="font-semibold text-slate-100">{doc.filename}</span>
            <p className="text-[11px] text-slate-500 font-mono mt-0.5">{doc.file_path}</p>
          </div>
        </div>
      ),
    },
    {
      key: 'file_type',
      header: 'Category',
      sortable: true,
      render: (doc) => (
        <span className="rounded bg-slate-900 px-2 py-0.5 font-mono text-[11px] text-slate-300 border border-slate-800 uppercase">
          {doc.file_type.replace('_', ' ')}
        </span>
      ),
    },
    {
      key: 'version',
      header: 'Version',
      render: (doc) => <span className="font-mono text-slate-300">v{doc.version}</span>,
    },
    {
      key: 'total_pages',
      header: 'Pages',
      render: (doc) => <span className="font-mono text-slate-300">{doc.total_pages} pgs</span>,
    },
    {
      key: 'file_size',
      header: 'Size',
      render: (doc) => (
        <span className="font-mono text-slate-400">
          {(doc.file_size / (1024 * 1024)).toFixed(2)} MB
        </span>
      ),
    },
    {
      key: 'status',
      header: 'Index Status',
      sortable: true,
      render: (doc) => <StatusBadge status={doc.status} />,
    },
    {
      key: 'actions',
      header: 'Inspection',
      render: (doc) => (
        <button
          onClick={() => handleInspectChunks(doc)}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-slate-800 bg-slate-900 hover:bg-slate-800 text-xs font-medium text-cyan-300 hover:text-cyan-200 transition-colors"
        >
          <Layers className="h-3.5 w-3.5 text-cyan-400" />
          <span>View Chunks</span>
        </button>
      ),
    },
  ];

  if (isLoading && documents.length === 0) {
    return <LoadingState message="Loading engineering specification documents..." />;
  }

  if (error && documents.length === 0) {
    return <ErrorState message={error} onRetry={loadDocuments} />;
  }

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Engineering Documents & Specifications' }]} />

      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-white">
            Document Repository & Specification Ingestion
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Centrally indexed engineering specifications, drawings, vendor submittals, and test procedures with pgvector embeddings.
          </p>
        </div>
      </div>

      <DataTable
        title="Indexed Project Documents"
        subtitle="Searchable specifications and vendor submittals"
        columns={columns}
        data={documents}
        searchKey={(doc) => `${doc.filename} ${doc.file_type}`}
        filterTabs={[
          { label: 'All Documents', value: 'all', filterFn: () => true },
          { label: 'Specifications', value: 'spec', filterFn: (d) => d.file_type === 'specification' },
          { label: 'Vendor Submittals', value: 'sub', filterFn: (d) => d.file_type === 'vendor_submittal' },
        ]}
      />

      {/* Chunks Inspection Modal / Drawer */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-150">
          <div className="w-full max-w-3xl max-h-[85vh] overflow-hidden rounded-2xl border border-slate-800 bg-slate-950 p-6 shadow-2xl flex flex-col space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <FileCode className="h-4 w-4 text-cyan-400" />
                  {selectedDoc.filename}
                </h3>
                <p className="text-xs text-slate-400 font-mono mt-0.5">
                  Extracted 768-dim Embeddings & Paragraph Chunks
                </p>
              </div>
              <button
                onClick={() => setSelectedDoc(null)}
                className="px-3 py-1 rounded-lg border border-slate-800 text-xs font-medium text-slate-400 hover:text-white hover:bg-slate-900"
              >
                Close
              </button>
            </div>

            <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar pr-2">
              {loadingChunks ? (
                <LoadingState message="Retrieving text chunks..." />
              ) : chunks.length > 0 ? (
                chunks.map((chunk) => (
                  <div key={chunk.id} className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-2">
                    <div className="flex items-center justify-between text-xs font-mono text-cyan-400">
                      <span>Chunk #{chunk.chunk_index} {chunk.page_number ? `(Page ${chunk.page_number})` : ''}</span>
                      <span className="text-slate-500 font-sans">{chunk.token_count} tokens</span>
                    </div>
                    {chunk.section_header && (
                      <p className="text-xs font-bold text-slate-200 uppercase tracking-wide">
                        {chunk.section_header}
                      </p>
                    )}
                    <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/60 p-3 rounded-lg border border-slate-800/60 font-mono">
                      {chunk.content}
                    </p>
                  </div>
                ))
              ) : (
                <div className="p-8 text-center text-xs text-slate-500">
                  No text chunks extracted yet for this document.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
