from fastapi import FastAPI
from app.api.v1.routes.router import api_router
from app.core.config import settings
from app.core.database import create_tables

create_tables()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)
