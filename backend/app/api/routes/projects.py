from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Project, Equipment
from app.schemas.project import ProjectRead
from app.schemas.equipment import EquipmentRead

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("/", response_model=List[ProjectRead])
def list_projects(db: Session = Depends(get_db)):
    """List all active EPC projects."""
    projects = db.query(Project).all()
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    """Retrieve specific EPC project details."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{project_id}/equipment", response_model=List[EquipmentRead])
def list_project_equipment(project_id: UUID, db: Session = Depends(get_db)):
    """List all major equipment items for a project."""
    equipment_items = db.query(Equipment).filter(Equipment.project_id == project_id).all()
    return equipment_items
