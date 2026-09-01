"""001_initial_schema: Create all 14 core EPC entities

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-02 01:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.models.base import GUID, get_vector_type

revision: str = "001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. Projects table
    op.create_table(
        "projects",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("code", sa.String(50), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("client", sa.String(255), nullable=True),
        sa.Column("contractor", sa.String(255), nullable=True),
        sa.Column("target_completion_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("total_budget", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(10), server_default="USD", nullable=False),
        sa.Column("status", sa.String(50), server_default="active", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_projects_code", "projects", ["code"])

    # 2. Documents table
    op.create_table(
        "documents",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("file_type", sa.String(50), nullable=False),
        sa.Column("file_size", sa.Integer(), server_default="0", nullable=False),
        sa.Column("mime_type", sa.String(100), server_default="application/pdf", nullable=False),
        sa.Column("checksum_md5", sa.String(64), nullable=True),
        sa.Column("version", sa.String(20), server_default="1.0", nullable=False),
        sa.Column("status", sa.String(50), server_default="uploaded", nullable=False),
        sa.Column("total_pages", sa.Integer(), server_default="0", nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_documents_project_id", "documents", ["project_id"])
    op.create_index("ix_documents_file_type", "documents", ["file_type"])

    # 3. Document Chunks table
    op.create_table(
        "document_chunks",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("document_id", GUID(), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=True),
        sa.Column("section_header", sa.String(255), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("token_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("embedding", get_vector_type(768), nullable=True),
        sa.Column("chunk_metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_document_chunks_document_id", "document_chunks", ["document_id"])

    # 4. Equipment table
    op.create_table(
        "equipment",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tag_number", sa.String(100), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("system_category", sa.String(100), nullable=False),
        sa.Column("specification_code", sa.String(100), nullable=True),
        sa.Column("location", sa.String(255), nullable=True),
        sa.Column("criticality", sa.String(50), server_default="high", nullable=False),
        sa.Column("status", sa.String(50), server_default="specified", nullable=False),
        sa.Column("technical_specs", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_equipment_project_id", "equipment", ["project_id"])
    op.create_index("ix_equipment_tag_number", "equipment", ["tag_number"])
    op.create_index("ix_equipment_system_category", "equipment", ["system_category"])

    # 5. Specification Requirements table
    op.create_table(
        "specification_requirements",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_id", GUID(), sa.ForeignKey("equipment.id", ondelete="CASCADE"), nullable=True),
        sa.Column("document_id", GUID(), sa.ForeignKey("documents.id", ondelete="SET NULL"), nullable=True),
        sa.Column("section_reference", sa.String(100), nullable=True),
        sa.Column("parameter_name", sa.String(255), nullable=False),
        sa.Column("operator", sa.String(20), nullable=False),
        sa.Column("target_value_numeric", sa.Float(), nullable=True),
        sa.Column("target_value_max", sa.Float(), nullable=True),
        sa.Column("target_value_text", sa.String(255), nullable=True),
        sa.Column("unit", sa.String(50), nullable=True),
        sa.Column("tolerance", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("is_mandatory", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_specification_requirements_project_id", "specification_requirements", ["project_id"])
    op.create_index("ix_specification_requirements_equipment_id", "specification_requirements", ["equipment_id"])
    op.create_index("ix_specification_requirements_parameter_name", "specification_requirements", ["parameter_name"])

    # 6. Vendor Submittals table
    op.create_table(
        "vendor_submittals",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_id", GUID(), sa.ForeignKey("equipment.id", ondelete="CASCADE"), nullable=True),
        sa.Column("document_id", GUID(), sa.ForeignKey("documents.id", ondelete="SET NULL"), nullable=True),
        sa.Column("submittal_number", sa.String(100), nullable=False),
        sa.Column("vendor_name", sa.String(255), nullable=False),
        sa.Column("model_number", sa.String(255), nullable=True),
        sa.Column("approval_status", sa.String(50), server_default="pending_review", nullable=False),
        sa.Column("extracted_data", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_vendor_submittals_project_id", "vendor_submittals", ["project_id"])
    op.create_index("ix_vendor_submittals_submittal_number", "vendor_submittals", ["submittal_number"])

    # 7. Compliance Checks table
    op.create_table(
        "compliance_checks",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("requirement_id", GUID(), sa.ForeignKey("specification_requirements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submittal_id", GUID(), sa.ForeignKey("vendor_submittals.id", ondelete="CASCADE"), nullable=True),
        sa.Column("equipment_id", GUID(), sa.ForeignKey("equipment.id", ondelete="CASCADE"), nullable=True),
        sa.Column("submitted_value_numeric", sa.Float(), nullable=True),
        sa.Column("submitted_value_text", sa.String(255), nullable=True),
        sa.Column("submitted_unit", sa.String(50), nullable=True),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("deviation_numeric", sa.Float(), nullable=True),
        sa.Column("deviation_description", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(50), server_default="low", nullable=False),
        sa.Column("ai_explanation", sa.Text(), nullable=True),
        sa.Column("recommended_action", sa.Text(), nullable=True),
        sa.Column("checked_by", sa.String(100), server_default="ComplianceEngine-v1", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_compliance_checks_project_id", "compliance_checks", ["project_id"])
    op.create_index("ix_compliance_checks_requirement_id", "compliance_checks", ["requirement_id"])
    op.create_index("ix_compliance_checks_status", "compliance_checks", ["status"])

    # 8. Schedule Activities table
    op.create_table(
        "schedule_activities",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_id", GUID(), sa.ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("activity_code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("wbs", sa.String(100), nullable=True),
        sa.Column("planned_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("planned_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actual_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("percent_complete", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("predecessors", sa.JSON(), nullable=False),
        sa.Column("successors", sa.JSON(), nullable=False),
        sa.Column("is_critical_path", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("status", sa.String(50), server_default="not_started", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_schedule_activities_project_id", "schedule_activities", ["project_id"])
    op.create_index("ix_schedule_activities_activity_code", "schedule_activities", ["activity_code"])
    op.create_index("ix_schedule_activities_is_critical_path", "schedule_activities", ["is_critical_path"])

    # 9. Procurement Items table
    op.create_table(
        "procurement_items",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_id", GUID(), sa.ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("po_number", sa.String(100), nullable=True),
        sa.Column("item_description", sa.String(255), nullable=False),
        sa.Column("supplier_name", sa.String(255), nullable=False),
        sa.Column("planned_order_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_order_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("lead_time_weeks", sa.Integer(), server_default="0", nullable=False),
        sa.Column("planned_factory_testing_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("planned_delivery_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expected_delivery_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actual_delivery_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(50), server_default="po_placed", nullable=False),
        sa.Column("cost", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(10), server_default="USD", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_procurement_items_project_id", "procurement_items", ["project_id"])
    op.create_index("ix_procurement_items_po_number", "procurement_items", ["po_number"])

    # 10. Risks table
    op.create_table(
        "risks",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_id", GUID(), sa.ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("activity_id", GUID(), sa.ForeignKey("schedule_activities.id", ondelete="SET NULL"), nullable=True),
        sa.Column("procurement_id", GUID(), sa.ForeignKey("procurement_items.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("risk_level", sa.String(50), nullable=False),
        sa.Column("risk_score", sa.Float(), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("impact_days", sa.Integer(), server_default="0", nullable=False),
        sa.Column("potential_cost_impact", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("root_cause", sa.Text(), nullable=True),
        sa.Column("downstream_impact_summary", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), server_default="active", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_risks_project_id", "risks", ["project_id"])
    op.create_index("ix_risks_risk_level", "risks", ["risk_level"])

    # 11. Risk Mitigations table
    op.create_table(
        "risk_mitigations",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("risk_id", GUID(), sa.ForeignKey("risks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("action_plan", sa.Text(), nullable=False),
        sa.Column("assigned_to", sa.String(100), nullable=True),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("estimated_cost", sa.Float(), server_default="0.0", nullable=False),
        sa.Column("status", sa.String(50), server_default="proposed", nullable=False),
        sa.Column("ai_recommended", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_risk_mitigations_risk_id", "risk_mitigations", ["risk_id"])

    # 12. RFIs table
    op.create_table(
        "rfis",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rfi_number", sa.String(100), nullable=False),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("suggested_answer", sa.Text(), nullable=True),
        sa.Column("official_response", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), server_default="open", nullable=False),
        sa.Column("priority", sa.String(50), server_default="medium", nullable=False),
        sa.Column("assigned_to", sa.String(100), nullable=True),
        sa.Column("date_raised", sa.DateTime(timezone=True), nullable=False),
        sa.Column("date_responded", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_rfis_project_id", "rfis", ["project_id"])
    op.create_index("ix_rfis_rfi_number", "rfis", ["rfi_number"])

    # 13. Commissioning Tests table
    op.create_table(
        "commissioning_tests",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_id", GUID(), sa.ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True),
        sa.Column("test_level", sa.String(50), nullable=False),
        sa.Column("test_code", sa.String(100), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("acceptance_criteria", sa.Text(), nullable=False),
        sa.Column("test_result", sa.String(50), server_default="pending", nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("tested_by", sa.String(100), nullable=True),
        sa.Column("witnessed_by", sa.String(100), nullable=True),
        sa.Column("test_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_commissioning_tests_project_id", "commissioning_tests", ["project_id"])
    op.create_index("ix_commissioning_tests_test_level", "commissioning_tests", ["test_level"])

    # 14. Audit Logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", GUID(), primary_key=True),
        sa.Column("project_id", GUID(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=True),
        sa.Column("entity_name", sa.String(100), nullable=False),
        sa.Column("entity_id", GUID(), nullable=True),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("performed_by", sa.String(100), server_default="system", nullable=False),
        sa.Column("details_json", sa.JSON(), nullable=False),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_audit_logs_project_id", "audit_logs", ["project_id"])
    op.create_index("ix_audit_logs_entity_name", "audit_logs", ["entity_name"])

def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("commissioning_tests")
    op.drop_table("rfis")
    op.drop_table("risk_mitigations")
    op.drop_table("risks")
    op.drop_table("procurement_items")
    op.drop_table("schedule_activities")
    op.drop_table("compliance_checks")
    op.drop_table("vendor_submittals")
    op.drop_table("specification_requirements")
    op.drop_table("equipment")
    op.drop_table("document_chunks")
    op.drop_table("documents")
    op.drop_table("projects")
