from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class RFIBase(BaseModel):
    rfi_number: str = Field(..., max_length=100)
    subject: str = Field(..., max_length=255)
    question: str
    suggested_answer: Optional[str] = None
    official_response: Optional[str] = None
    status: str = "open"
    priority: str = "medium"
    assigned_to: Optional[str] = None
    date_raised: Optional[datetime] = None
    date_responded: Optional[datetime] = None


class RFICreate(RFIBase):
    project_id: UUID


class RFIRead(RFIBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommissioningTestBase(BaseModel):
    test_level: str = Field(..., max_length=50)
    test_code: str = Field(..., max_length=100)
    name: str = Field(..., max_length=255)
    acceptance_criteria: str
    test_result: str = "pending"
    notes: Optional[str] = None
    tested_by: Optional[str] = None
    witnessed_by: Optional[str] = None
    test_date: Optional[datetime] = None


class CommissioningTestCreate(CommissioningTestBase):
    project_id: UUID
    equipment_id: Optional[UUID] = None


class CommissioningTestRead(CommissioningTestBase):
    id: UUID
    project_id: UUID
    equipment_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogRead(BaseModel):
    id: UUID
    project_id: Optional[UUID] = None
    entity_name: str
    entity_id: Optional[UUID] = None
    action: str
    performed_by: str
    details_json: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
