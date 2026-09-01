from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import ScheduleActivity
from app.schemas.schedule import ScheduleActivityRead

router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.get("/activities", response_model=List[ScheduleActivityRead])
def list_schedule_activities(project_id: UUID = None, critical_only: bool = False, db: Session = Depends(get_db)):
    """List schedule activities and critical path milestones."""
    query = db.query(ScheduleActivity)
    if project_id:
        query = query.filter(ScheduleActivity.project_id == project_id)
    if critical_only:
        query = query.filter(ScheduleActivity.is_critical_path == True)
    return query.order_by(ScheduleActivity.planned_start).all()
