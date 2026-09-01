from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models import (
    Project,
    Equipment,
    ComplianceCheck,
    ScheduleActivity,
    ProcurementItem,
    Risk,
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def get_dashboard_summary(project_id: UUID = None, db: Session = Depends(get_db)):
    """Retrieve dynamic high-level project intelligence metrics."""
    project = None
    if project_id:
        project = db.query(Project).filter(Project.id == project_id).first()
    else:
        project = db.query(Project).first()

    if not project:
        return {
            "status": "no_projects",
            "project_name": "No Project Seeded",
            "project_health": {"schedule": 100, "procurement": 100, "quality": 100, "commissioning": 100},
            "compliance_summary": {"total_checks": 0, "passed": 0, "failed": 0, "warnings": 0},
            "risk_summary": {"total_risks": 0, "critical": 0, "high": 0, "medium": 0, "low": 0},
            "recent_alerts": [],
        }

    pid = project.id

    # Compliance counts
    comp_total = db.query(ComplianceCheck).filter(ComplianceCheck.project_id == pid).count()
    comp_pass = db.query(ComplianceCheck).filter(ComplianceCheck.project_id == pid, ComplianceCheck.status == "PASS").count()
    comp_fail = db.query(ComplianceCheck).filter(ComplianceCheck.project_id == pid, ComplianceCheck.status == "FAIL").count()
    comp_warn = db.query(ComplianceCheck).filter(ComplianceCheck.project_id == pid, ComplianceCheck.status == "WARNING").count()

    # Risk counts
    risks_total = db.query(Risk).filter(Risk.project_id == pid).count()
    risks_critical = db.query(Risk).filter(Risk.project_id == pid, Risk.risk_level == "CRITICAL").count()
    risks_high = db.query(Risk).filter(Risk.project_id == pid, Risk.risk_level == "HIGH").count()
    risks_medium = db.query(Risk).filter(Risk.project_id == pid, Risk.risk_level == "MEDIUM").count()
    risks_low = db.query(Risk).filter(Risk.project_id == pid, Risk.risk_level == "LOW").count()

    # Delayed items
    delayed_activities = db.query(ScheduleActivity).filter(ScheduleActivity.project_id == pid, ScheduleActivity.status == "delayed").count()
    delayed_procurement = db.query(ProcurementItem).filter(ProcurementItem.project_id == pid, ProcurementItem.status.in_(["customs_hold", "delayed"])).count()

    # Dynamic health scoring
    schedule_health = max(0, 100 - (delayed_activities * 20 + risks_critical * 15))
    procurement_health = max(0, 100 - (delayed_procurement * 25))
    quality_health = max(0, int((comp_pass / comp_total * 100))) if comp_total > 0 else 100

    # Recent alerts
    alerts = []
    if comp_fail > 0:
        alerts.append({
            "type": "compliance_fail",
            "severity": "critical",
            "message": f"{comp_fail} Critical Specification Non-Conformance(s) Detected",
        })
    if risks_critical > 0:
        alerts.append({
            "type": "schedule_risk",
            "severity": "critical",
            "message": f"{risks_critical} Critical Path Risk(s) Exceeding 14 Days Delay Impact",
        })
    if delayed_procurement > 0:
        alerts.append({
            "type": "procurement_delay",
            "severity": "high",
            "message": f"{delayed_procurement} Equipment Package(s) on Customs Hold",
        })

    return {
        "status": "active",
        "project_id": str(project.id),
        "project_name": project.name,
        "project_code": project.code,
        "target_completion_date": project.target_completion_date.isoformat() if project.target_completion_date else None,
        "project_health": {
            "schedule": schedule_health,
            "procurement": procurement_health,
            "quality": quality_health,
            "commissioning": 95,
        },
        "compliance_summary": {
            "total_checks": comp_total,
            "passed": comp_pass,
            "failed": comp_fail,
            "warnings": comp_warn,
        },
        "risk_summary": {
            "total_risks": risks_total,
            "critical": risks_critical,
            "high": risks_high,
            "medium": risks_medium,
            "low": risks_low,
        },
        "recent_alerts": alerts,
    }
