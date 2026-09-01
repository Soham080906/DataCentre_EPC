from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ScheduleActivityBase(BaseModel):
    activity_code: str = Field(..., max_length=100)
    name: str = Field(..., max_length=255)
    wbs: Optional[str] = None
    planned_start: datetime
    planned_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    duration_days: int
    percent_complete: float = 0.0
    predecessors: List[str] = Field(default_factory=list)
    successors: List[str] = Field(default_factory=list)
    is_critical_path: bool = False
    status: str = "not_started"


class ScheduleActivityCreate(ScheduleActivityBase):
    project_id: UUID
    equipment_id: Optional[UUID] = None


class ScheduleActivityRead(ScheduleActivityBase):
    id: UUID
    project_id: UUID
    equipment_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProcurementItemBase(BaseModel):
    po_number: Optional[str] = None
    item_description: str = Field(..., max_length=255)
    supplier_name: str = Field(..., max_length=255)
    planned_order_date: Optional[datetime] = None
    actual_order_date: Optional[datetime] = None
    lead_time_weeks: int = 0
    planned_factory_testing_date: Optional[datetime] = None
    planned_delivery_date: datetime
    expected_delivery_date: datetime
    actual_delivery_date: Optional[datetime] = None
    status: str = "po_placed"
    cost: Optional[float] = None
    currency: str = "USD"


class ProcurementItemCreate(ProcurementItemBase):
    project_id: UUID
    equipment_id: Optional[UUID] = None


class ProcurementItemRead(ProcurementItemBase):
    id: UUID
    project_id: UUID
    equipment_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
