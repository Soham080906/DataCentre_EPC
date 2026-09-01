from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Risk
from app.schemas.risk import RiskRead

router = APIRouter(prefix="/risks", tags=["Schedule Risks"])


@router.get("/", response_model=List[RiskRead])
def list_risks(project_id: UUID = None, level: str = None, db: Session = Depends(get_db)):
    """List calculated schedule, procurement, compliance, and delivery risks."""
    query = db.query(Risk)
    if project_id:
        query = query.filter(Risk.project_id == project_id)
    if level:
        query = query.filter(Risk.risk_level == level.upper())
    return query.order_by(Risk.risk_score.desc()).all()


@router.get("/{risk_id}", response_model=RiskRead)
def get_risk(risk_id: UUID, db: Session = Depends(get_db)):
    """Retrieve detailed risk profile and downstream impact assessment."""
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    return risk
