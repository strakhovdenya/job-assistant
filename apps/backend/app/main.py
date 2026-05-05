from fastapi import FastAPI

from app.api.routes_health import router as health_router
from app.api.routes_raw_jobs import router as raw_jobs_router
from app.api.routes_jobs import router as jobs_router
from app.api.routes_ai_extraction import router as ai_extraction_router
from app.api.routes_job_drafts import router as job_drafts_router

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

# Временно для Sprint 1.
# Позже заменишь это на Alembic migrations.
# Base.metadata.create_all(bind=engine)

app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(raw_jobs_router, prefix=settings.api_v1_prefix)
app.include_router(jobs_router, prefix=settings.api_v1_prefix)
app.include_router(ai_extraction_router)
app.include_router(job_drafts_router)
