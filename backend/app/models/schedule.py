import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import GUID, TimestampMixin


class ScheduleActivity(Base, TimestampMixin):
    """Critical path schedule activity (Primavera P6 / MS Project)."""
    __tablename__ = "schedule_activities"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id = Column(GUID, ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True, index=True)

    activity_code = Column(String(100), nullable=False, index=True) # e.g. 'ACT-1040'
    name = Column(String(255), nullable=False) # e.g. 'UPS System Rigging & Setting'
    wbs = Column(String(100), nullable=True) # e.g. '1.3.2.1'
    planned_start = Column(DateTime(timezone=True), nullable=False)
    planned_end = Column(DateTime(timezone=True), nullable=False)
    actual_start = Column(DateTime(timezone=True), nullable=True)
    actual_end = Column(DateTime(timezone=True), nullable=True)
    duration_days = Column(Integer, nullable=False)
    percent_complete = Column(Float, default=0.0, nullable=False)

    predecessors = Column(JSON, default=list, nullable=False) # list of activity_codes
    successors = Column(JSON, default=list, nullable=False)
    is_critical_path = Column(Boolean, default=False, nullable=False, index=True)
    status = Column(String(50), default="not_started", nullable=False) # 'not_started', 'in_progress', 'completed', 'delayed'

    # Relationships
    project = relationship("Project", back_populates="schedule_activities")
    equipment = relationship("Equipment", back_populates="schedule_activities")
    risks = relationship("Risk", back_populates="activity")

    def __repr__(self):
        return f"<ScheduleActivity code={self.activity_code} name={self.name} critical={self.is_critical_path}>"


class ProcurementItem(Base, TimestampMixin):
    """Procurement item tracking PO, factory testing, lead times, and on-site delivery."""
    __tablename__ = "procurement_items"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    project_id = Column(GUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    equipment_id = Column(GUID, ForeignKey("equipment.id", ondelete="SET NULL"), nullable=True, index=True)

    po_number = Column(String(100), nullable=True, index=True) # 'PO-2026-DC-089'
    item_description = Column(String(255), nullable=False)
    supplier_name = Column(String(255), nullable=False)
    planned_order_date = Column(DateTime(timezone=True), nullable=True)
    actual_order_date = Column(DateTime(timezone=True), nullable=True)
    lead_time_weeks = Column(Integer, default=0, nullable=False)

    planned_factory_testing_date = Column(DateTime(timezone=True), nullable=True)
    planned_delivery_date = Column(DateTime(timezone=True), nullable=False)
    expected_delivery_date = Column(DateTime(timezone=True), nullable=False)
    actual_delivery_date = Column(DateTime(timezone=True), nullable=True)

    status = Column(String(50), default="po_placed", nullable=False, index=True) # 'rfq', 'po_placed', 'manufacturing', 'fat_passed', 'in_transit', 'delivered'
    cost = Column(Float, nullable=True)
    currency = Column(String(10), default="USD", nullable=False)

    # Relationships
    project = relationship("Project", back_populates="procurement_items")
    equipment = relationship("Equipment", back_populates="procurement_items")
    risks = relationship("Risk", back_populates="procurement_item")

    def __repr__(self):
        return f"<ProcurementItem po={self.po_number} item={self.item_description} status={self.status}>"
