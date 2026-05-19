from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/", response_model=CategoryResponse)
async def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    category = service.create_category(category_data)
    return category

@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    categories = service.get_all_categories()
    return categories