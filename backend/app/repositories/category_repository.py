from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category_schema import CategoryCreate


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db


    def create_category(
        self,
        category_data: CategoryCreate
    ) -> Category:

        category = Category(
            name=category_data.name,
            type=category_data.type
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)

        return category