from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class SpecificationRequirementBase(BaseModel):
    section_reference: Optional[str] = None
    parameter_name: str = Field(..., max_length=255)
    operator: str = Field(..., max_length=20)
    target_value_numeric: Optional[float] = None
    target_value_max: Optional[float] = None
    target_value_text: Optional[str] = None
    unit: Optional[str] = None
    tolerance: float = 0.0
    is_mandatory: bool = True
    description: Optional[str] = None


class SpecificationRequirementCreate(SpecificationRequirementBase):
    project_id: UUID
    equipment_id: Optional[UUID] = None
    document_id: Optional[UUID] = None


class SpecificationRequirementRead(SpecificationRequirementBase):
    id: UUID
    project_id: UUID
    equipment_id: Optional[UUID] = None
    document_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VendorSubmittalBase(BaseModel):
    submittal_number: str = Field(..., max_length=100)
    vendor_name: str = Field(..., max_length=255)
    model_number: Optional[str] = None
    approval_status: str = "pending_review"
    extracted_data: Dict[str, Any] = Field(default_factory=dict)


class VendorSubmittalCreate(VendorSubmittalBase):
    project_id: UUID
    equipment_id: Optional[UUID] = None
    document_id: Optional[UUID] = None


class VendorSubmittalRead(VendorSubmittalBase):
    id: UUID
    project_id: UUID
    equipment_id: Optional[UUID] = None
    document_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ComplianceCheckBase(BaseModel):
    submitted_value_numeric: Optional[float] = None
    submitted_value_text: Optional[str] = None
    submitted_unit: Optional[str] = None
    status: str = Field(..., max_length=50) # 'PASS', 'FAIL', 'WARNING', 'NOT ENOUGH DATA'
    deviation_numeric: Optional[float] = None
    deviation_description: Optional[str] = None
    severity: str = "low"
    ai_explanation: Optional[str] = None
    recommended_action: Optional[str] = None
    checked_by: str = "ComplianceEngine-v1"


class ComplianceCheckCreate(ComplianceCheckBase):
    project_id: UUID
    requirement_id: UUID
    submittal_id: Optional[UUID] = None
    equipment_id: Optional[UUID] = None


class ComplianceCheckRead(ComplianceCheckBase):
    id: UUID
    project_id: UUID
    requirement_id: UUID
    submittal_id: Optional[UUID] = None
    equipment_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
