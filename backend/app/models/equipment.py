import uuid
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import GUID, TimestampMixin


class Equipment(Base, TimestampMixin):
    """Major Data Centre equipment items (UPS, Generators, Chillers, Transformers, CRAHs, Switchgear)."""
    __tablename__ = "equipment"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    tag_number = Column(String(100), nullable=False, index=True) # e.g., 'UPS-01A', 'GEN-01', 'CH-01'
    name = Column(String(255), nullable=False) # e.g., 'Uninterruptible Power Supply 2000kVA'
    system_category = Column(String(100), nullable=False, index=True) # 'Electrical', 'Mechanical / HVAC', 'Fire & Safety'
    specification_code = Column(String(100), nullable=True) # e.g. '26 33 53'
    location = Column(String(255), nullable=True) # e.g. 'Electrical Room 101'
    criticality = Column(String(50), default="high", nullable=False) # 'low', 'medium', 'high', 'critical'
    status = Column(String(50), default="specified", nullable=False) # 'specified', 'procured', 'delivered', 'installed', 'tested', 'commissioned'
    technical_specs = Column(JSON, default=dict, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="equipment")
    procurement_items = relationship("ProcurementItem", back_populates="equipment", cascade="all, delete-orphan")
    specification_requirements = relationship("SpecificationRequirement", back_populates="equipment", cascade="all, delete-orphan")
    vendor_submittals = relationship("VendorSubmittal", back_populates="equipment", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="equipment", cascade="all, delete-orphan")
    schedule_activities = relationship("ScheduleActivity", back_populates="equipment")
    commissioning_tests = relationship("CommissioningTest", back_populates="equipment", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="equipment")

    def __repr__(self):
        return f"<Equipment tag={self.tag_number} name={self.name}>"
