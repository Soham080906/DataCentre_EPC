from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class RiskMitigationBase(BaseModel):
    action_plan: str
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_cost: float = 0.0
    status: str = "proposed"
    ai_recommended: bool = True


class RiskMitigationCreate(RiskMitigationBase):
    risk_id: UUID


class RiskMitigationRead(RiskMitigationBase):
    id: UUID
    risk_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RiskBase(BaseModel):
    title: str = Field(..., max_length=255)
    category: str = Field(..., max_length=100)
    risk_level: str = Field(..., max_length=50) # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    risk_score: float = Field(..., ge=0.0, le=100.0)
    probability: float = Field(..., ge=0.0, le=1.0)
    impact_days: int = 0
    potential_cost_impact: float = 0.0
    root_cause: Optional[str] = None
    downstream_impact_summary: Optional[str] = None
    status: str = "active"


class RiskCreate(RiskBase):
    project_id: UUID
    equipment_id: Optional[UUID] = None
    activity_id: Optional[UUID] = None
    procurement_id: Optional[UUID] = None


class RiskRead(RiskBase):
    id: UUID
    project_id: UUID
    equipment_id: Optional[UUID] = None
    activity_id: Optional[UUID] = None
    procurement_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
