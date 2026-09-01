from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class EquipmentBase(BaseModel):
    tag_number: str = Field(..., max_length=100)
    name: str = Field(..., max_length=255)
    system_category: str = Field(..., max_length=100)
    specification_code: Optional[str] = None
    location: Optional[str] = None
    criticality: str = "high"
    status: str = "specified"
    technical_specs: Dict[str, Any] = Field(default_factory=dict)


class EquipmentCreate(EquipmentBase):
    project_id: UUID


class EquipmentRead(EquipmentBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
