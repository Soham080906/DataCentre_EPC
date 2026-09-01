import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import GUID, TimestampMixin


class RFI(Base, TimestampMixin):
    """Request For Information (RFI) regarding engineering drawings or specifications."""
    __tablename__ = "rfis"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)

    rfi_number = Column(String(100), nullable=False, index=True) # e.g. 'RFI-ELEC-042'
    subject = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    suggested_answer = Column(Text, nullable=True)
    official_response = Column(Text, nullable=True)
    status = Column(String(50), default="open", nullable=False, index=True) # 'open', 'under_review', 'answered', 'closed'
    priority = Column(String(50), default="medium", nullable=False) # 'low', 'medium', 'high', 'urgent'
    assigned_to = Column(String(100), nullable=True)
    date_raised = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    date_responded = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="rfis")

    def __repr__(self):
        return f"<RFI num={self.rfi_number} subject={self.subject} status={self.status}>"


class CommissioningTest(Base, TimestampMixin):
    """Quality and commissioning test matrix records (Level 1 to Level 5 IST)."""
    __tablename__ = "commissioning_tests"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id = Column(GUID, ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True, index=True)

    test_level = Column(String(50), nullable=False, index=True) # 'Level 1 - FAT', 'Level 2 - Receipt', 'Level 3 - Pre-Functional', 'Level 4 - Functional', 'Level 5 - IST'
    test_code = Column(String(100), nullable=False, index=True) # e.g. 'IST-ELEC-UPS-001'
    name = Column(String(255), nullable=False)
    acceptance_criteria = Column(Text, nullable=False)
    test_result = Column(String(50), default="pending", nullable=False, index=True) # 'pending', 'PASS', 'FAIL', 'CONDITIONAL_PASS'
    notes = Column(Text, nullable=True)
    tested_by = Column(String(100), nullable=True)
    witnessed_by = Column(String(100), nullable=True)
    test_date = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="commissioning_tests")
    equipment = relationship("Equipment", back_populates="commissioning_tests")

    def __repr__(self):
        return f"<CommissioningTest code={self.test_code} level={self.test_level} result={self.test_result}>"


class AuditLog(Base):
    """System-wide immutable audit trail for tracking actions, compliance checks, and model modifications."""
    __tablename__ = "audit_logs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True, index=True)
    entity_name = Column(String(100), nullable=False, index=True) # 'ComplianceCheck', 'ScheduleActivity'
    entity_id = Column(GUID, nullable=True)
    action = Column(String(50), nullable=False, index=True) # 'CREATE', 'UPDATE', 'DELETE', 'COMPLIANCE_RUN', 'RISK_CALCULATED'
    performed_by = Column(String(100), default="system", nullable=False)
    details_json = Column(JSON, default=dict, nullable=False)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    project = relationship("Project", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog entity={self.entity_name} action={self.action} by={self.performed_by}>"
