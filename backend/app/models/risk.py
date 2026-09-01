import uuid
from sqlalchemy import Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import GUID, TimestampMixin


class Risk(Base, TimestampMixin):
    """Calculated schedule, procurement, quality, and delivery risks."""
    __tablename__ = "risks"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id = Column(GUID, ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True, index=True)
    activity_id = Column(GUID, ForeignKey("schedule_activities.id", ondelete="SET NULL"), nullable=True, index=True)
    procurement_id = Column(GUID, ForeignKey("procurement_items.id", ondelete="SET NULL"), nullable=True, index=True)

    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False, index=True) # 'schedule', 'procurement', 'compliance', 'commissioning'
    risk_level = Column(String(50), nullable=False, index=True) # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    risk_score = Column(Float, nullable=False) # 0.0 to 100.0
    probability = Column(Float, nullable=False) # 0.0 to 1.0
    impact_days = Column(Integer, default=0, nullable=False)
    potential_cost_impact = Column(Float, default=0.0, nullable=False)

    root_cause = Column(Text, nullable=True)
    downstream_impact_summary = Column(Text, nullable=True)
    status = Column(String(50), default="active", nullable=False) # 'active', 'mitigated', 'accepted', 'closed'

    # Relationships
    project = relationship("Project", back_populates="risks")
    equipment = relationship("Equipment", back_populates="risks")
    activity = relationship("ScheduleActivity", back_populates="risks")
    procurement_item = relationship("ProcurementItem", back_populates="risks")
    mitigations = relationship("RiskMitigation", back_populates="risk", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Risk title={self.title} level={self.risk_level} score={self.risk_score}>"


class RiskMitigation(Base, TimestampMixin):
    """Specific mitigation actions and recovery plans for identified risks."""
    __tablename__ = "risk_mitigations"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    risk_id = Column(GUID, ForeignKey("risks.id", ondelete="CASCADE"), nullable=False, index=True)
    action_plan = Column(Text, nullable=False)
    assigned_to = Column(String(100), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    estimated_cost = Column(Float, default=0.0, nullable=False)
    status = Column(String(50), default="proposed", nullable=False) # 'proposed', 'in_progress', 'completed', 'verified'
    ai_recommended = Column(Boolean, default=True, nullable=False)

    # Relationships
    risk = relationship("Risk", back_populates="mitigations")

    def __repr__(self):
        return f"<RiskMitigation risk={self.risk_id} status={self.status}>"
