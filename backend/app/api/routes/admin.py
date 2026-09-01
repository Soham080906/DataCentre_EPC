from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.seed_data import seed_database

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/seed")
def trigger_seed_database(db: Session = Depends(get_db)):
    """Seed the database with comprehensive sample project data."""
    project_id = seed_database(db=db)
    return {
        "status": "success",
        "message": "Database seeded successfully with 50MW Hyperscale Data Centre project data",
        "project_id": str(project_id),
    }
