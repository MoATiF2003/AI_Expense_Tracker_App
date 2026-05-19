from fastapi import APIRouter
from app.api.v1.routes.health_routes import router as health_router
from app.api.v1.routes.test_db_routes import router as test_db_routes
from app.api.v1.routes.account_routes import router as account_routes
from app.api.v1.routes.category_routes import router as category_routes
from app.api.v1.routes.transaction_routes import router as transaction_routes

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(test_db_routes)
api_router.include_router(account_routes)
api_router.include_router(category_routes)
api_router.include_router(transaction_routes)