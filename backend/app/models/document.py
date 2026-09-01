import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import GUID, TimestampMixin, get_vector_type


class Document(Base, TimestampMixin):
    """Project engineering documentation (Specifications, Vendor Submittals, Drawings, Test Protocols)."""
    __tablename__ = "documents"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False, index=True) # 'specification', 'vendor_submittal', 'drawing', 'procedure'
    file_size = Column(Integer, default=0, nullable=False)
    mime_type = Column(String(100), default="application/pdf", nullable=False)
    checksum_md5 = Column(String(64), nullable=True)
    version = Column(String(20), default="1.0", nullable=False)
    status = Column(String(50), default="uploaded", nullable=False) # 'uploaded', 'processing', 'indexed', 'error'
    total_pages = Column(Integer, default=0, nullable=False)
    metadata_json = Column(JSON, default=dict, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    specification_requirements = relationship("SpecificationRequirement", back_populates="document")
    vendor_submittals = relationship("VendorSubmittal", back_populates="document")

    def __repr__(self):
        return f"<Document id={self.id} filename={self.filename} type={self.file_type}>"


class DocumentChunk(Base, TimestampMixin):
    """Text chunk from document extraction with 768-dim vector embeddings for RAG retrieval."""
    __tablename__ = "document_chunks"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    document_id = Column(GUID, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    page_number = Column(Integer, nullable=True)
    section_header = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, default=0, nullable=False)
    embedding = Column(get_vector_type(768), nullable=True)
    chunk_metadata = Column(JSON, default=dict, nullable=False)

    # Relationships
    document = relationship("Document", back_populates="chunks")

    def __repr__(self):
        return f"<DocumentChunk doc={self.document_id} idx={self.chunk_index} page={self.page_number}>"
