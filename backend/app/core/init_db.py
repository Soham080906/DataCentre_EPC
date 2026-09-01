import logging
from sqlalchemy import text
from app.core.database import engine, Base
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

logger = logging.getLogger(__name__)


def init_db():
    """Create all database tables and extensions if not already present."""
    logger.info("Initializing database schema and extensions...")
    with engine.begin() as conn:
        # Enable pgvector and uuid-ossp if running on PostgreSQL
        if conn.dialect.name == "postgresql":
            try:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"vector\";"))
                logger.info("PostgreSQL uuid-ossp and vector extensions verified.")
            except Exception as e:
                logger.warning(f"Could not enable PostgreSQL extensions (might require superuser): {e}")

    # Create all tables registered with declarative Base
    Base.metadata.create_all(bind=engine)
    logger.info("All 14 entity tables created or verified successfully.")


if __name__ == "__main__":
    init_db()
