from fastapi import APIRouter
from app.api.v1.routes.health_routes import router as health_router
from app.api.v1.routes.test_db_routes import router as test_db_routes

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(test_db_routes)