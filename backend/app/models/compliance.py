import uuid
from sqlalchemy import Column, String, Text, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import GUID, TimestampMixin


class SpecificationRequirement(Base, TimestampMixin):
    """Extracted technical requirements from specifications (e.g. UPS Efficiency >= 96.5%)."""
    __tablename__ = "specification_requirements"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id = Column(GUID, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=True, index=True)
    document_id = Column(GUID, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True)
    section_reference = Column(String(100), nullable=True)
    parameter_name = Column(String(255), nullable=False, index=True) # 'efficiency', 'cop', 'voltage_tolerance'
    operator = Column(String(20), nullable=False) # '>=', '<=', '==', 'min', 'max', 'range'
    target_value_numeric = Column(Float, nullable=True) # 96.5
    target_value_max = Column(Float, nullable=True)
    target_value_text = Column(String(255), nullable=True)
    unit = Column(String(50), nullable=True) # '%', 'kW', 'TR', 'degC'
    tolerance = Column(Float, default=0.0, nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="specification_requirements")
    equipment = relationship("Equipment", back_populates="specification_requirements")
    document = relationship("Document", back_populates="specification_requirements")
    compliance_checks = relationship("ComplianceCheck", back_populates="requirement", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SpecRequirement {self.parameter_name} {self.operator} {self.target_value_numeric} {self.unit}>"


class VendorSubmittal(Base, TimestampMixin):
    """Vendor technical submission documents & extracted values."""
    __tablename__ = "vendor_submittals"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id = Column(GUID, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=True, index=True)
    document_id = Column(GUID, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True, index=True)
    submittal_number = Column(String(100), nullable=False, index=True) # 'SUB-ELEC-UPS-001'
    vendor_name = Column(String(255), nullable=False) # 'Vertiv / Schneider Electric'
    model_number = Column(String(255), nullable=True)
    approval_status = Column(String(50), default="pending_review", nullable=False) # 'pending_review', 'approved', 'rejected'
    extracted_data = Column(JSON, default=dict, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="vendor_submittals")
    equipment = relationship("Equipment", back_populates="vendor_submittals")
    document = relationship("Document", back_populates="vendor_submittals")
    compliance_checks = relationship("ComplianceCheck", back_populates="submittal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<VendorSubmittal num={self.submittal_number} vendor={self.vendor_name}>"


class ComplianceCheck(Base, TimestampMixin):
    """Automated comparison result between a Specification Requirement and a Vendor Submittal."""
    __tablename__ = "compliance_checks"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    requirement_id = Column(GUID, ForeignKey("specification_requirements.id", ondelete="CASCADE"), nullable=False, index=True)
    submittal_id = Column(GUID, ForeignKey("vendor_submittals.id", ondelete="CASCADE"), nullable=True, index=True)
    equipment_id = Column(GUID, ForeignKey("equipment.id", ondelete="CASCADE"), nullable=True, index=True)

    submitted_value_numeric = Column(Float, nullable=True) # 94.0
    submitted_value_text = Column(String(255), nullable=True)
    submitted_unit = Column(String(50), nullable=True)

    status = Column(String(50), nullable=False, index=True) # 'PASS', 'FAIL', 'WARNING', 'NOT ENOUGH DATA'
    deviation_numeric = Column(Float, nullable=True) # -2.5
    deviation_description = Column(Text, nullable=True)
    severity = Column(String(50), default="low", nullable=False) # 'low', 'medium', 'high', 'critical'

    ai_explanation = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    checked_by = Column(String(100), default="ComplianceEngine-v1", nullable=False)

    # Relationships
    project = relationship("Project", back_populates="compliance_checks")
    requirement = relationship("SpecificationRequirement", back_populates="compliance_checks")
    submittal = relationship("VendorSubmittal", back_populates="compliance_checks")
    equipment = relationship("Equipment", back_populates="compliance_checks")

    def __repr__(self):
        return f"<ComplianceCheck req={self.requirement_id} status={self.status}>"
