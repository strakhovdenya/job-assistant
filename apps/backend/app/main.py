from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_raw_jobs import router as raw_jobs_router
from app.api.routes_jobs import router as jobs_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

settings = get_settings()

app = FastAPI(title=settings.app_name)

# Временно для Sprint 1.
# Позже заменишь это на Alembic migrations.
# Base.metadata.create_all(bind=engine)

app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(raw_jobs_router, prefix=settings.api_v1_prefix)
app.include_router(jobs_router, prefix=settings.api_v1_prefix)