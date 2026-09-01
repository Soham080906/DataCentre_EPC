from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class DocumentChunkRead(BaseModel):
    id: UUID
    document_id: UUID
    chunk_index: int
    page_number: Optional[int] = None
    section_header: Optional[str] = None
    content: str
    token_count: int = 0
    chunk_metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentBase(BaseModel):
    filename: str = Field(..., max_length=255)
    file_type: str = Field(..., max_length=50)
    file_size: int = 0
    mime_type: str = "application/pdf"
    version: str = "1.0"
    status: str = "uploaded"
    total_pages: int = 0
    metadata_json: Dict[str, Any] = Field(default_factory=dict)


class DocumentCreate(DocumentBase):
    project_id: UUID
    file_path: str


class DocumentRead(DocumentBase):
    id: UUID
    project_id: UUID
    file_path: str
    checksum_md5: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
