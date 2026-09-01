from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import ProcurementItem
from app.schemas.schedule import ProcurementItemRead

router = APIRouter(prefix="/procurement", tags=["Procurement"])


@router.get("/items", response_model=List[ProcurementItemRead])
def list_procurement_items(project_id: UUID = None, db: Session = Depends(get_db)):
    """List equipment procurement items, lead times, and tracking status."""
    query = db.query(ProcurementItem)
    if project_id:
        query = query.filter(ProcurementItem.project_id == project_id)
    return query.order_by(ProcurementItem.expected_delivery_date).all()
