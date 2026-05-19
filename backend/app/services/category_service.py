from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate

class CategoryService:

    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def create_category(
        self,
        category_data: CategoryCreate
    ):
        return self.repository.create_category(category_data)
    
    def get_all_categories(self):
        return self.repository.get_all_categories()