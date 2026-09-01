import uuid
from sqlalchemy import Column, String, Text, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import GUID, TimestampMixin


class Project(Base, TimestampMixin):
    """Core Project entity representing a Data Centre EPC Build (e.g. 50MW Hyperscale Campus)."""
    __tablename__ = "projects"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    client = Column(String(255), nullable=True)
    contractor = Column(String(255), nullable=True)
    target_completion_date = Column(DateTime(timezone=True), nullable=True)
    total_budget = Column(Float, nullable=True)
    currency = Column(String(10), default="USD", nullable=False)
    status = Column(String(50), default="active", nullable=False)

    # Relationships with cascading deletes
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    equipment = relationship("Equipment", back_populates="project", cascade="all, delete-orphan")
    schedule_activities = relationship("ScheduleActivity", back_populates="project", cascade="all, delete-orphan")
    procurement_items = relationship("ProcurementItem", back_populates="project", cascade="all, delete-orphan")
    rfis = relationship("RFI", back_populates="project", cascade="all, delete-orphan")
    specification_requirements = relationship("SpecificationRequirement", back_populates="project", cascade="all, delete-orphan")
    vendor_submittals = relationship("VendorSubmittal", back_populates="project", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="project", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="project", cascade="all, delete-orphan")
    commissioning_tests = relationship("CommissioningTest", back_populates="project", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project code={self.code} name={self.name}>"
