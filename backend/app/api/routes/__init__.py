from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.projects import router as projects_router
from app.api.routes.documents import router as documents_router
from app.api.routes.chat import router as chat_router
from app.api.routes.compliance import router as compliance_router
from app.api.routes.schedule import router as schedule_router
from app.api.routes.procurement import router as procurement_router
from app.api.routes.risks import router as risks_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.admin import router as admin_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(projects_router)
api_router.include_router(documents_router)
api_router.include_router(chat_router)
api_router.include_router(compliance_router)
api_router.include_router(schedule_router)
api_router.include_router(procurement_router)
api_router.include_router(risks_router)
api_router.include_router(dashboard_router)
api_router.include_router(admin_router)
