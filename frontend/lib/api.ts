import axios from 'axios';
import {
  HealthResponse,
  Project,
  Equipment,
  Document,
  DocumentChunk,
  SpecificationRequirement,
  VendorSubmittal,
  ComplianceCheck,
  ScheduleActivity,
  ProcurementItem,
  Risk,
  DashboardSummary,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await apiClient.get<HealthResponse>('/health');
  return response.data;
}

export async function fetchPing(): Promise<{ ping: string; time: string }> {
  const response = await apiClient.get('/ping');
  return response.data;
}

export async function fetchProjects(): Promise<Project[]> {
  const response = await apiClient.get<Project[]>('/projects/');
  return response.data;
}

export async function fetchProject(id: string): Promise<Project> {
  const response = await apiClient.get<Project>(`/projects/${id}`);
  return response.data;
}

export async function fetchProjectEquipment(projectId: string): Promise<Equipment[]> {
  const response = await apiClient.get<Equipment[]>(`/projects/${projectId}/equipment`);
  return response.data;
}

export async function fetchDashboardSummary(projectId?: string): Promise<DashboardSummary> {
  const params = projectId ? { project_id: projectId } : {};
  const response = await apiClient.get<DashboardSummary>('/dashboard/summary', { params });
  return response.data;
}

export async function fetchDocuments(projectId?: string): Promise<Document[]> {
  const params = projectId ? { project_id: projectId } : {};
  const response = await apiClient.get<Document[]>('/documents/', { params });
  return response.data;
}

export async function fetchDocument(id: string): Promise<Document> {
  const response = await apiClient.get<Document>(`/documents/${id}`);
  return response.data;
}

export async function fetchDocumentChunks(id: string): Promise<DocumentChunk[]> {
  const response = await apiClient.get<DocumentChunk[]>(`/documents/${id}/chunks`);
  return response.data;
}

export async function fetchComplianceResults(projectId?: string): Promise<ComplianceCheck[]> {
  const params = projectId ? { project_id: projectId } : {};
  const response = await apiClient.get<ComplianceCheck[]>('/compliance/results', { params });
  return response.data;
}

export async function fetchSpecificationRequirements(projectId?: string): Promise<SpecificationRequirement[]> {
  const params = projectId ? { project_id: projectId } : {};
  const response = await apiClient.get<SpecificationRequirement[]>('/compliance/requirements', { params });
  return response.data;
}

export async function fetchVendorSubmittals(projectId?: string): Promise<VendorSubmittal[]> {
  const params = projectId ? { project_id: projectId } : {};
  const response = await apiClient.get<VendorSubmittal[]>('/compliance/submittals', { params });
  return response.data;
}

export async function fetchScheduleActivities(projectId?: string, criticalOnly?: boolean): Promise<ScheduleActivity[]> {
  const params: Record<string, any> = {};
  if (projectId) params.project_id = projectId;
  if (criticalOnly) params.critical_only = true;
  const response = await apiClient.get<ScheduleActivity[]>('/schedule/activities', { params });
  return response.data;
}

export async function fetchProcurementItems(projectId?: string): Promise<ProcurementItem[]> {
  const params = projectId ? { project_id: projectId } : {};
  const response = await apiClient.get<ProcurementItem[]>('/procurement/items', { params });
  return response.data;
}

export async function fetchRisks(projectId?: string, level?: string): Promise<Risk[]> {
  const params: Record<string, any> = {};
  if (projectId) params.project_id = projectId;
  if (level) params.level = level;
  const response = await apiClient.get<Risk[]>('/risks/', { params });
  return response.data;
}

export async function fetchRisk(id: string): Promise<Risk> {
  const response = await apiClient.get<Risk>(`/risks/${id}`);
  return response.data;
}

export async function triggerSeedDatabase(): Promise<{ status: string; message: string; project_id: string }> {
  const response = await apiClient.post('/admin/seed');
  return response.data;
}
