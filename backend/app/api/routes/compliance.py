from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import ComplianceCheck, SpecificationRequirement, VendorSubmittal
from app.schemas.compliance import ComplianceCheckRead, SpecificationRequirementRead, VendorSubmittalRead

router = APIRouter(prefix="/compliance", tags=["Specification Compliance"])


@router.get("/results", response_model=List[ComplianceCheckRead])
def list_compliance_results(project_id: UUID = None, db: Session = Depends(get_db)):
    """List all specification compliance checks (PASS, FAIL, WARNING)."""
    query = db.query(ComplianceCheck)
    if project_id:
        query = query.filter(ComplianceCheck.project_id == project_id)
    return query.all()


@router.get("/results/{check_id}", response_model=ComplianceCheckRead)
def get_compliance_result(check_id: UUID, db: Session = Depends(get_db)):
    """Retrieve specific compliance verification breakdown."""
    check = db.query(ComplianceCheck).filter(ComplianceCheck.id == check_id).first()
    if not check:
        raise HTTPException(status_code=404, detail="Compliance check record not found")
    return check


@router.get("/requirements", response_model=List[SpecificationRequirementRead])
def list_specification_requirements(project_id: UUID = None, db: Session = Depends(get_db)):
    """List extracted technical specification requirements."""
    query = db.query(SpecificationRequirement)
    if project_id:
        query = query.filter(SpecificationRequirement.project_id == project_id)
    return query.all()


@router.get("/submittals", response_model=List[VendorSubmittalRead])
def list_vendor_submittals(project_id: UUID = None, db: Session = Depends(get_db)):
    """List vendor submittal packages."""
    query = db.query(VendorSubmittal)
    if project_id:
        query = query.filter(VendorSubmittal.project_id == project_id)
    return query.all()
