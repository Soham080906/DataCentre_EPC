import uuid
import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app
from app.models import (
    Project,
    Document,
    DocumentChunk,
    Equipment,
    SpecificationRequirement,
    VendorSubmittal,
    ComplianceCheck,
    ScheduleActivity,
    ProcurementItem,
    Risk,
    RiskMitigation,
    RFI,
    CommissioningTest,
    AuditLog,
)
from app.core.seed_data import seed_database

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for a test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """TestClient with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_and_query_project(db_session):
    """Verify Project creation and UUID primary key."""
    proj = Project(
        name="Test 20MW DC",
        code="TEST-DC20",
        description="Test project",
        total_budget=150000000.0,
    )
    db_session.add(proj)
    db_session.commit()

    queried = db_session.query(Project).filter(Project.code == "TEST-DC20").first()
    assert queried is not None
    assert isinstance(queried.id, uuid.UUID)
    assert queried.name == "Test 20MW DC"
    assert queried.created_at is not None


def test_equipment_and_relationships(db_session):
    """Verify Equipment model and foreign-key relationship to Project."""
    proj = Project(name="Project Alpha", code="ALPHA-01")
    db_session.add(proj)
    db_session.flush()

    eq = Equipment(
        project_id=proj.id,
        tag_number="UPS-01A",
        name="Static UPS 2000kVA",
        system_category="Electrical",
        criticality="critical",
    )
    db_session.add(eq)
    db_session.commit()

    assert len(proj.equipment) == 1
    assert proj.equipment[0].tag_number == "UPS-01A"
    assert proj.equipment[0].project.code == "ALPHA-01"


def test_specification_and_compliance_check(db_session):
    """Verify SpecRequirement -> VendorSubmittal -> ComplianceCheck link."""
    proj = Project(name="Project Beta", code="BETA-01")
    db_session.add(proj)
    db_session.flush()

    eq = Equipment(project_id=proj.id, tag_number="GEN-01", name="Generator 2500kVA", system_category="Electrical")
    db_session.add(eq)
    db_session.flush()

    req = SpecificationRequirement(
        project_id=proj.id,
        equipment_id=eq.id,
        parameter_name="start_time",
        operator="<=",
        target_value_numeric=10.0,
        unit="sec",
    )
    db_session.add(req)
    db_session.flush()

    sub = VendorSubmittal(
        project_id=proj.id,
        equipment_id=eq.id,
        submittal_number="SUB-GEN-01",
        vendor_name="Caterpillar",
        extracted_data={"start_time": 8.5},
    )
    db_session.add(sub)
    db_session.flush()

    check = ComplianceCheck(
        project_id=proj.id,
        requirement_id=req.id,
        submittal_id=sub.id,
        equipment_id=eq.id,
        submitted_value_numeric=8.5,
        submitted_unit="sec",
        status="PASS",
        severity="low",
    )
    db_session.add(check)
    db_session.commit()

    assert len(req.compliance_checks) == 1
    assert req.compliance_checks[0].status == "PASS"
    assert sub.compliance_checks[0].submitted_value_numeric == 8.5


def test_schedule_procurement_risk_cascade(db_session):
    """Verify ScheduleActivity, ProcurementItem, Risk, and RiskMitigation linking."""
    proj = Project(name="Project Gamma", code="GAMMA-01")
    db_session.add(proj)
    db_session.flush()

    now = datetime.now(timezone.utc)
    act = ScheduleActivity(
        project_id=proj.id,
        activity_code="ACT-01",
        name="Transformer Installation",
        planned_start=now,
        planned_end=now,
        duration_days=14,
        is_critical_path=True,
    )
    proc = ProcurementItem(
        project_id=proj.id,
        item_description="25MVA Power Transformer",
        supplier_name="Siemens",
        planned_delivery_date=now,
        expected_delivery_date=now,
        status="customs_hold",
    )
    db_session.add_all([act, proc])
    db_session.flush()

    risk = Risk(
        project_id=proj.id,
        activity_id=act.id,
        procurement_id=proc.id,
        title="Customs Hold Delay",
        category="procurement",
        risk_level="CRITICAL",
        risk_score=85.0,
        probability=0.9,
    )
    db_session.add(risk)
    db_session.flush()

    mit = RiskMitigation(
        risk_id=risk.id,
        action_plan="Expedite customs clearance broker bond",
        assigned_to="Logistics Lead",
    )
    db_session.add(mit)
    db_session.commit()

    assert len(risk.mitigations) == 1
    assert risk.mitigations[0].action_plan == "Expedite customs clearance broker bond"


def test_seed_database_execution(db_session):
    """Verify seed_database populates all 14 entities correctly."""
    project_id = seed_database(db=db_session)
    assert project_id is not None

    proj = db_session.query(Project).filter(Project.id == project_id).first()
    assert proj.code == "TITAN-DC01"

    # Verify counts
    assert db_session.query(Equipment).filter(Equipment.project_id == project_id).count() >= 5
    assert db_session.query(SpecificationRequirement).filter(SpecificationRequirement.project_id == project_id).count() >= 5
    assert db_session.query(ScheduleActivity).filter(ScheduleActivity.project_id == project_id).count() >= 5
    assert db_session.query(ProcurementItem).filter(ProcurementItem.project_id == project_id).count() >= 5
    assert db_session.query(ComplianceCheck).filter(ComplianceCheck.project_id == project_id).count() >= 4
    assert db_session.query(Risk).filter(Risk.project_id == project_id).count() >= 2
    assert db_session.query(RFI).filter(RFI.project_id == project_id).count() >= 2
    assert db_session.query(CommissioningTest).filter(CommissioningTest.project_id == project_id).count() >= 2


def test_api_routes_with_seeded_data(client, db_session):
    """Verify REST API routes return real database entities."""
    seed_database(db=db_session)

    # 1. Projects API
    res = client.get("/api/projects/")
    assert res.status_code == 200
    projects = res.json()
    assert len(projects) >= 1
    assert projects[0]["code"] == "TITAN-DC01"

    # 2. Compliance API
    res_comp = client.get("/api/compliance/results")
    assert res_comp.status_code == 200
    checks = res_comp.json()
    assert len(checks) >= 4
    statuses = [c["status"] for c in checks]
    assert "FAIL" in statuses
    assert "PASS" in statuses

    # 3. Schedule API
    res_sch = client.get("/api/schedule/activities")
    assert res_sch.status_code == 200
    activities = res_sch.json()
    assert len(activities) >= 7

    # 4. Procurement API
    res_proc = client.get("/api/procurement/items")
    assert res_proc.status_code == 200
    items = res_proc.json()
    assert len(items) >= 5

    # 5. Risks API
    res_risk = client.get("/api/risks/")
    assert res_risk.status_code == 200
    risks = res_risk.json()
    assert len(risks) >= 2

    # 6. Dashboard Summary API
    res_dash = client.get("/api/dashboard/summary")
    assert res_dash.status_code == 200
    dash = res_dash.json()
    assert dash["status"] == "active"
    assert dash["project_code"] == "TITAN-DC01"
    assert dash["compliance_summary"]["total_checks"] >= 4
    assert dash["risk_summary"]["total_risks"] >= 2
