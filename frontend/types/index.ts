export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'error';
  project: string;
  version: string;
  environment: string;
  timestamp: string;
  services: {
    database: {
      status: string;
      database_url?: string;
      error?: string;
    };
    llm_provider: {
      provider: string;
      model: string;
      configured: boolean;
    };
    vector_store: {
      backend: string;
      collection: string;
    };
    storage: {
      backend: string;
      directory: string;
    };
  };
}

export interface Project {
  id: string;
  name: string;
  code: string;
  description?: string | null;
  location?: string | null;
  client?: string | null;
  contractor?: string | null;
  target_completion_date?: string | null;
  total_budget?: number | null;
  currency: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Equipment {
  id: string;
  project_id: string;
  tag_number: string;
  name: string;
  system_category: string;
  specification_code?: string | null;
  location?: string | null;
  criticality: 'low' | 'medium' | 'high' | 'critical';
  status: 'specified' | 'procured' | 'delivered' | 'installed' | 'tested' | 'commissioned';
  technical_specs: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: string;
  project_id: string;
  filename: string;
  file_path: string;
  file_type: 'specification' | 'vendor_submittal' | 'drawing' | 'procedure' | string;
  file_size: number;
  mime_type: string;
  checksum_md5?: string | null;
  version: string;
  status: 'uploaded' | 'processing' | 'indexed' | 'error';
  total_pages: number;
  metadata_json: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface DocumentChunk {
  id: string;
  document_id: string;
  chunk_index: number;
  page_number?: number | null;
  section_header?: string | null;
  content: string;
  token_count: number;
  chunk_metadata: Record<string, any>;
  created_at: string;
}

export interface SpecificationRequirement {
  id: string;
  project_id: string;
  equipment_id?: string | null;
  document_id?: string | null;
  section_reference?: string | null;
  parameter_name: string;
  operator: string;
  target_value_numeric?: number | null;
  target_value_max?: number | null;
  target_value_text?: string | null;
  unit?: string | null;
  tolerance: number;
  is_mandatory: boolean;
  description?: string | null;
  created_at: string;
  updated_at: string;
}

export interface VendorSubmittal {
  id: string;
  project_id: string;
  equipment_id?: string | null;
  document_id?: string | null;
  submittal_number: string;
  vendor_name: string;
  model_number?: string | null;
  approval_status: 'pending_review' | 'approved' | 'approved_with_notes' | 'rejected' | string;
  extracted_data: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface ComplianceCheck {
  id: string;
  project_id: string;
  requirement_id: string;
  submittal_id?: string | null;
  equipment_id?: string | null;
  submitted_value_numeric?: number | null;
  submitted_value_text?: string | null;
  submitted_unit?: string | null;
  status: 'PASS' | 'FAIL' | 'WARNING' | 'NOT ENOUGH DATA' | string;
  deviation_numeric?: number | null;
  deviation_description?: string | null;
  severity: 'low' | 'medium' | 'high' | 'critical' | string;
  ai_explanation?: string | null;
  recommended_action?: string | null;
  checked_by: string;
  created_at: string;
  updated_at: string;
}

export interface ScheduleActivity {
  id: string;
  project_id: string;
  equipment_id?: string | null;
  activity_code: string;
  name: string;
  wbs?: string | null;
  planned_start: string;
  planned_end: string;
  actual_start?: string | null;
  actual_end?: string | null;
  duration_days: number;
  percent_complete: number;
  predecessors: string[];
  successors: string[];
  is_critical_path: boolean;
  status: 'not_started' | 'in_progress' | 'completed' | 'delayed' | string;
  created_at: string;
  updated_at: string;
}

export interface ProcurementItem {
  id: string;
  project_id: string;
  equipment_id?: string | null;
  po_number?: string | null;
  item_description: string;
  supplier_name: string;
  planned_order_date?: string | null;
  actual_order_date?: string | null;
  lead_time_weeks: number;
  planned_factory_testing_date?: string | null;
  planned_delivery_date: string;
  expected_delivery_date: string;
  actual_delivery_date?: string | null;
  status: 'rfq' | 'po_placed' | 'manufacturing' | 'fat_passed' | 'in_transit' | 'delivered' | 'customs_hold' | string;
  cost?: number | null;
  currency: string;
  created_at: string;
  updated_at: string;
}

export interface RiskMitigation {
  id: string;
  risk_id: string;
  action_plan: string;
  assigned_to?: string | null;
  due_date?: string | null;
  estimated_cost: number;
  status: 'proposed' | 'in_progress' | 'completed' | 'verified' | string;
  ai_recommended: boolean;
  created_at: string;
  updated_at: string;
}

export interface Risk {
  id: string;
  project_id: string;
  equipment_id?: string | null;
  activity_id?: string | null;
  procurement_id?: string | null;
  title: string;
  category: 'schedule' | 'procurement' | 'compliance' | 'commissioning' | string;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_score: number;
  probability: number;
  impact_days: number;
  potential_cost_impact: number;
  root_cause?: string | null;
  downstream_impact_summary?: string | null;
  status: 'active' | 'mitigated' | 'accepted' | 'closed' | string;
  mitigations?: RiskMitigation[];
  created_at: string;
  updated_at: string;
}

export interface RFI {
  id: string;
  project_id: string;
  rfi_number: string;
  subject: string;
  question: string;
  suggested_answer?: string | null;
  official_response?: string | null;
  status: 'open' | 'under_review' | 'answered' | 'closed' | string;
  priority: 'low' | 'medium' | 'high' | 'urgent' | string;
  assigned_to?: string | null;
  date_raised: string;
  date_responded?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CommissioningTest {
  id: string;
  project_id: string;
  equipment_id?: string | null;
  test_level: string;
  test_code: string;
  name: string;
  acceptance_criteria: string;
  test_result: 'pending' | 'PASS' | 'FAIL' | 'CONDITIONAL_PASS' | string;
  notes?: string | null;
  tested_by?: string | null;
  witnessed_by?: string | null;
  test_date?: string | null;
  created_at: string;
  updated_at: string;
}

export interface DashboardAlert {
  type: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  message: string;
}

export interface DashboardSummary {
  status: string;
  project_id?: string;
  project_name?: string;
  project_code?: string;
  target_completion_date?: string | null;
  project_health: {
    schedule: number;
    procurement: number;
    quality: number;
    commissioning: number;
  };
  compliance_summary: {
    total_checks: number;
    passed: number;
    failed: number;
    warnings: number;
  };
  risk_summary: {
    total_risks: number;
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  recent_alerts: DashboardAlert[];
}
