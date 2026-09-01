from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.core.database import check_db_connection
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
def get_health() -> HealthResponse:
    """Return backend health status and dependent service availability."""
    db_status = check_db_connection()
    overall_status = "healthy" if db_status.get("status") == "connected" else "degraded"

    return HealthResponse(
        status=overall_status,
        project=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc),
        services={
            "database": db_status,
            "llm_provider": {
                "provider": settings.LLM_PROVIDER,
                "model": settings.LLM_MODEL,
                "configured": bool(settings.LLM_API_KEY),
            },
            "vector_store": {
                "backend": settings.VECTOR_STORE_BACKEND,
                "collection": settings.VECTOR_COLLECTION_NAME,
            },
            "storage": {
                "backend": settings.STORAGE_BACKEND,
                "directory": settings.LOCAL_STORAGE_DIR,
            },
        },
    )


@router.get("/ping", tags=["Health"])
def ping():
    """Simple lightweight ping for liveness probes."""
    return {"ping": "pong", "time": datetime.now(timezone.utc).isoformat()}
