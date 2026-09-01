import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app
from app.core.seed_data import seed_database

TEST_DB_URL = "sqlite:///:memory:"
engine_test = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine_test)
    session = TestSession()
    seed_database(db=session)
    session.close()

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)


def test_cors_headers_configured(client):
    """Verify CORS headers permit frontend at localhost:3000."""
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_structured_error_handling_404(client):
    """Verify 404 error response follows structured JSON schema."""
    response = client.get("/api/nonexistent-endpoint")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] is True
    assert data["code"] == "HTTP_404"


def test_all_stub_routes_accessible(client):
    """Verify all REST routes return successful 200 OK responses with database backing."""
    endpoints = [
        "/api/projects/",
        "/api/documents/",
        "/api/compliance/results",
        "/api/compliance/requirements",
        "/api/compliance/submittals",
        "/api/schedule/activities",
        "/api/procurement/items",
        "/api/risks/",
        "/api/dashboard/summary",
    ]
    for endpoint in endpoints:
        res = client.get(endpoint)
        assert res.status_code == 200, f"Endpoint {endpoint} failed with status {res.status_code}: {res.text}"
