from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=50)
    description: Optional[str] = None
    location: Optional[str] = None
    client: Optional[str] = None
    contractor: Optional[str] = None
    target_completion_date: Optional[datetime] = None
    total_budget: Optional[float] = None
    currency: str = "USD"
    status: str = "active"


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    client: Optional[str] = None
    contractor: Optional[str] = None
    target_completion_date: Optional[datetime] = None
    total_budget: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None


class ProjectRead(ProjectBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
